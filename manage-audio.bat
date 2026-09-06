@echo off
setlocal
cd /d "%~dp0"

title Grammar Explorer - Audio Track Manager

echo.
echo ===================================================
echo   Grammar Explorer - Audio Track Manager
echo ===================================================
echo.

node manage-audio.js %*

echo.
pause
