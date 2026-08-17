@echo off
REM ============================================================================
REM  ai-powered-crm - Windows startup script
REM  Double-click this file to set up and launch the application.
REM ============================================================================

setlocal enabledelayedexpansion
title ai-powered-crm - Starting up...
cd /d "%~dp0"

echo.
echo ==========================================================
echo   ai-powered-crm  -  AI-Powered CRM
echo ==========================================================
echo.

REM ----------------------------------------------------------------------
REM 1. Check whether Python is installed
REM ----------------------------------------------------------------------
echo [1/6] Checking for Python...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python was not found on your system.
    echo.
    echo Please install Python 3.11 or newer from:
    echo   https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check the box that says
    echo "Add python.exe to PATH" before clicking Install.
    echo.
    goto :error_exit
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PY_VERSION=%%v
echo       Found Python %PY_VERSION%
echo.

REM ----------------------------------------------------------------------
REM 2. Create the virtual environment if it doesn't exist yet
REM ----------------------------------------------------------------------
echo [2/6] Checking for virtual environment...
if not exist ".venv\Scripts\activate.bat" (
    echo       Creating virtual environment in .venv ...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Failed to create the virtual environment.
        goto :error_exit
    )
    echo       Virtual environment created.
) else (
    echo       Virtual environment already exists.
)
echo.

REM ----------------------------------------------------------------------
REM 3. Activate the virtual environment
REM ----------------------------------------------------------------------
echo [3/6] Activating virtual environment...
call ".venv\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to activate the virtual environment.
    goto :error_exit
)
echo       Activated.
echo.

REM ----------------------------------------------------------------------
REM 4. Install / verify dependencies
REM ----------------------------------------------------------------------
echo [4/6] Installing dependencies from requirements.txt...
echo       (this may take a minute the first time)
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies. Check your internet
    echo connection and the messages above, then try again.
    goto :error_exit
)
echo       Dependencies OK.
echo.

REM ----------------------------------------------------------------------
REM 5. Verify the .env file
REM ----------------------------------------------------------------------
echo [5/6] Checking for .env configuration file...
if not exist ".env" (
    if exist ".env.example" (
        echo       No .env file found - creating one from .env.example ...
        copy /y ".env.example" ".env" >nul
        echo       Created .env with default settings.
        echo       Edit .env and add your OPENAI_API_KEY to enable AI features.
    ) else (
        echo       [WARNING] No .env or .env.example file found.
        echo       The app will run with built-in defaults.
    )
) else (
    echo       .env file found.
)
echo.

REM ----------------------------------------------------------------------
REM 6. Launch the application
REM ----------------------------------------------------------------------
echo [6/6] Starting ai-powered-crm...
echo.
echo ==========================================================
echo   The app will open at:  http://127.0.0.1:8000
echo   Press CTRL+C in this window to stop the server.
echo ==========================================================
echo.

start "" "http://127.0.0.1:8000"
uvicorn app.main:app --host 127.0.0.1 --port 8000

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The application exited with an error. See the messages
    echo above for details.
    goto :error_exit
)

goto :eof

:error_exit
echo.
echo -----------------------------------------------------------
echo  Something went wrong. Read the message above for details.
echo  This window will stay open so you can review it.
echo -----------------------------------------------------------
pause
exit /b 1
