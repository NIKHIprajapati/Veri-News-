@echo off
title VeriNews Launcher
echo ===================================================
echo               Launching VeriNews
echo ===================================================
echo.
echo Starting Backend (Flask API) on http://127.0.0.1:5000 ...
start "VeriNews Backend" "%~dp0run-backend.bat"

timeout /t 2 /nobreak >nul

echo Starting Frontend (React Vite) on http://localhost:5173 ...
start "VeriNews Frontend" "%~dp0run-frontend.bat"

echo.
echo ===================================================
echo   Both Frontend and Backend are starting up!
echo   Close this window or press any key to exit.
echo ===================================================
timeout /t 5 >nul
