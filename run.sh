#!/bin/bash

# Quick run script for TCSinger2 Demo App

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Run the demo app
echo "🎵 Starting TCSinger2 Demo App..."
python app/demo.py "$@"
