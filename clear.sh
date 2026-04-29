#!/bin/bash
echo -e "\033]0;WebControl - Clear Data\007"

echo "Clearing WebControl user data..."

# Remove database
if [ -f "webcontrol.db" ]; then
    rm -f webcontrol.db
    echo "Database cleared."
fi

# Remove logs
if [ -d "logs" ]; then
    rm -f logs/*.log
    echo "Logs cleared."
fi

# Remove screenshots
if [ -d "static/screenshots" ]; then
    rm -f static/screenshots/*.png
    rm -f static/screenshots/*.jpg
    echo "Screenshots cleared."
fi

echo ""
echo "All user data has been cleared!"
