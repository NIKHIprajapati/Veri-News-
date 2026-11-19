@echo off
title VeriNews Backend
cd /d "%~dp0backend"
echo ===================================================
echo             Starting VeriNews Backend
echo ===================================================
echo Backend URL: http://127.0.0.1:5000
echo.
python app.py
pause
