@echo off
setlocal
cd /d "%~dp0"

title Grammar Explorer - Audio Track Manager

echo ===================================================
echo   Grammar Explorer - Audio Track & Git Manager
echo ===================================================
echo.

if "%~1"=="" goto interactive_mode

:: Direct command execution if arguments are provided (e.g. manage-audio.bat --check, manage-audio.bat --list, manage-audio.bat --apply --push)
node manage-audio.js %*
goto handle_exit

:interactive_mode
:: Interactive session with continuous addition loop & Git changes inspection
node manage-audio.js

:handle_exit
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] An error occurred during audio management operation.
    echo.
) else (
    echo.
    echo [SUCCESS] Operation finished successfully!
    echo.
)

pause
