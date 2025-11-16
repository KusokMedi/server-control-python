@echo off
echo ========================================
echo        WebControl Server Starter
echo ========================================
echo Starting WebControl server...
echo If the server crashes, it will restart automatically.
echo Press Ctrl+C to stop.
echo ========================================
:loop
python run.py
echo ========================================
echo Server stopped. Restarting...
echo ========================================
goto loop