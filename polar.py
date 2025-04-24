#!/usr/bin/env python3
import json
import os
import glob
from pathlib import Path
import math

def calculate_speed(vmg, angle):
    """Calculate boat speed from VMG and wind angle."""
    # Convert angle to radians
    angle_rad = math.radians(angle)
    # Speed = VMG / |cos(angle)| to ensure positive speed
    return vmg / abs(math.cos(angle_rad))

def convert_json_to_pol(json_path, pol_path):
    """Convert a JSON file to POL format for sailboat polar data."""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Extract VPP data
        vpp = data.get('vpp', {})
        angles = vpp.get('angles', [])
        speeds = vpp.get('speeds', [])
        
        # Extract beat and run data
        beat_angles = vpp.get('beat_angle', [])
        beat_vmgs = vpp.get('beat_vmg', [])
        run_angles = vpp.get('run_angle', [])
        run_vmgs = vpp.get('run_vmg', [])
        
        # Sort angles and speeds to ensure consistent order
        angles = sorted(angles)
        speeds = sorted(speeds)
        
        with open(pol_path, 'w') as f:
            # Write POL file header
            f.write("# Polar data for sailboat\n")
            f.write(f"# {data.get('name', 'Unknown')} - {data.get('boat', {}).get('type', 'Unknown')}\n")
            
            # Write TWS values as header
            f.write("TWA\\TWS\t")
            f.write("\t".join(str(speed) for speed in speeds))
            f.write("\n")
            
            # Write beat data first
            for tws, beat_angle, beat_vmg in zip(speeds, beat_angles, beat_vmgs):
                boat_speed = calculate_speed(beat_vmg, beat_angle)
                f.write(f"{beat_angle:.1f}\t")
                # Create a row with boat speed at the correct TWS column
                row = ['0.00'] * len(speeds)
                row[speeds.index(tws)] = f"{boat_speed:.2f}"
                f.write("\t".join(row))
                f.write("\n")
            
            # Write TWA and corresponding boat speeds
            for angle in angles:
                # Get the speed data for this angle
                speed_data = vpp.get(str(angle), [])
                if speed_data:
                    f.write(f"{angle}\t")
                    f.write("\t".join(str(speed) for speed in speed_data))
                    f.write("\n")
            
            # Write run data last
            for tws, run_angle, run_vmg in zip(speeds, run_angles, run_vmgs):
                boat_speed = calculate_speed(run_vmg, run_angle)
                f.write(f"{run_angle:.1f}\t")
                # Create a row with boat speed at the correct TWS column
                row = ['0.00'] * len(speeds)
                row[speeds.index(tws)] = f"{boat_speed:.2f}"
                f.write("\t".join(row))
                f.write("\n")
                
    except Exception as e:
        print(f"Error converting {json_path}: {str(e)}")

def main():
    # Get all JSON files in site/data/ and its subdirectories
    json_files = glob.glob('site/data/**/*.json', recursive=True)
    
    for json_file in json_files:
        # Create corresponding POL file path
        pol_file = os.path.splitext(json_file)[0] + '.pol'
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(pol_file), exist_ok=True)
        
        print(f"Converting {json_file} to {pol_file}")
        convert_json_to_pol(json_file, pol_file)

if __name__ == "__main__":
    main() 