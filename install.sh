#!/bin/bash

echo "Installing WebControl dependencies..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies with break-system-packages flag
pip install -r requirements.txt --break-system-packages

echo "Installation complete!"
echo "Run: source venv/bin/activate && python main.py"
