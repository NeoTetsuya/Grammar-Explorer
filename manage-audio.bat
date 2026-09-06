@echo off
setlocal
cd /d "%~dp0"

title Grammar Explorer - Audio Track Manager

if "%~1"=="" goto interactive_mode

:: Direct command execution if arguments are provided (e.g. manage-audio.bat --list)
node manage-audio.js %*
goto end

:interactive_mode
:: Interactive session with continuous addition loop
node manage-audio.js

:end
echo.
pause

