@echo off
:: =============================================================================
::  Global License Manager - Cyberpunk Animated Launcher
:: =============================================================================
::  Author  : Vicky Dhale
::  Theme   : Neon / Cyberpunk / Hacker Style
:: =============================================================================

title GLOBAL LICENSE MANAGER - CYBER LAUNCHER
color 0b
setlocal enabledelayedexpansion
cd /d "%~dp0"

:: ===============================
:: CYBER HEADER
:: ===============================
cls
echo.
echo  ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗     
echo ██╔════╝ ██║     ██╔════╝ ██╔══██╗██╔══██╗██║     
echo ██║  ███╗██║     ██║  ███╗██████╔╝███████║██║     
echo ██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║     
echo ╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗
echo  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
echo.
echo =====================================================
echo        GLOBAL LICENSE MANAGER - PRO EDITION
echo =====================================================
echo        Developer : Vicky Dhale
echo        Initializing Cyber Environment...
echo =====================================================
echo.

timeout /t 1 >nul

:: ===============================
:: FAKE LOADING ANIMATION
:: ===============================
set "bar="
for /l %%A in (1,1,30) do (
    set "bar=!bar!#"
    cls
    echo.
    echo [ CYBER SYSTEM BOOTING ]
    echo.
    echo !bar!
    timeout /t 0 >nul
)

echo.
echo [ OK ] Core Modules Loaded.
timeout /t 1 >nul

:: ===============================
:: CHECK PYTHON
:: ===============================
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ ERROR ] Python not detected in system PATH.
    echo Install Python and try again.
    pause
    exit /b 1
)

:: ===============================
:: ACTIVATE VENV
:: ===============================
if exist "venv\Scripts\activate.bat" (
    echo [ INFO ] Activating Virtual Environment...
    call venv\Scripts\activate.bat
    timeout /t 1 >nul
)

:: ===============================
:: RUN APPLICATION
:: ===============================
echo.
echo [ LAUNCHING ] Global License Manager...
timeout /t 1 >nul

python run.py

:: ===============================
:: EXIT MESSAGE
:: ===============================
echo.
echo =====================================================
echo      CYBER SESSION TERMINATED
echo      Thank you for using GLM
echo =====================================================
echo.
pause
endlocal