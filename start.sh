#!/bin/bash
echo -e "\033]0;WebControl - Starting...\007"

echo "Starting WebControl..."

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the application
python main.py
