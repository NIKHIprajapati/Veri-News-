@echo off
title VeriNews Frontend
cd /d "%~dp0frontend"
echo ===================================================
echo             Starting VeriNews Frontend
echo ===================================================
echo Frontend URL: http://localhost:5173
echo.
npm run dev
pause
