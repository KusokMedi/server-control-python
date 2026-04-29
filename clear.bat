@echo off
title WebControl - Clear Data
echo Clearing WebControl user data...

REM Remove database
if exist webcontrol.db del /F /Q webcontrol.db
echo Database cleared.

REM Remove logs
if exist logs\*.log del /F /Q logs\*.log
echo Logs cleared.

REM Remove screenshots
if exist static\screenshots\*.png del /F /Q static\screenshots\*.png
if exist static\screenshots\*.jpg del /F /Q static\screenshots\*.jpg
echo Screenshots cleared.

echo.
echo All user data has been cleared!
pause
