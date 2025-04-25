#!/bin/bash

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed. Please install Node.js and npm first."
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Build the project if the build directory doesn't exist
if [ ! -d "site/build" ]; then
    echo "Building the project..."
    npm run build
fi

# Start the server on port 4567
echo "Starting server on http://localhost:4567"
npx sirv site --port 4567 --no-clear 