@echo off
title NGROK Autoreconnect (port 5000)

:LOOP
echo ================================
echo Запуск ngrok на порту 5000...
echo ================================
ngrok http 5000 --pooling-enabled

echo Ngrok is stopped. Reconect in 3s..
timeout /t 3 >nul
goto LOOP
