@echo off
title VeriNews One-Time Setup
echo ===================================================
echo             VeriNews One-Time Setup
echo ===================================================
echo.
echo [1/2] Installing Python backend packages...
pip install -r "%~dp0backend\requirements.txt"
echo.
echo [2/2] Installing Frontend Node.js dependencies...
cd /d "%~dp0frontend"
call npm install
cd /d "%~dp0"
echo.
echo ===================================================
echo   Setup Complete!
echo   You can now launch the project using run.bat
echo ===================================================
pause
