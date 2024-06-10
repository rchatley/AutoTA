#!/bin/bash

# Ensure the script stops on any error
set -e

# Function to print a message and exit with an error code
error_exit() {
    echo "$1" 1>&2
    exit 1
}

# Check if Python is installed
if ! command -v python &>/dev/null; then
    error_exit "Python is not installed or not added to PATH."
fi

# Install required packages from requirements.txt if available
if [ -f requirements.txt ]; then
    echo "Installing required packages..."
    python -m pip install --upgrade pip || error_exit "Failed to upgrade pip."
    python -m pip install -r requirements.txt || error_exit "Failed to install required packages."
else
    echo "requirements.txt not found. Ensure all dependencies are installed."
fi

# Construct the arguments string
args=""
while [[ "$1" != "" ]]; do
    args="$args $1"
    shift
done

# Running the Python script with arguments
python autoReview.py "$args" || error_exit "Failed to run autoReview.py."