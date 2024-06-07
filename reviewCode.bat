@echo off
REM This line ensures that any errors in the batch file are shown in the command prompt
setlocal enabledelayedexpansion

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not added to PATH.
    pause
    exit /b 1
)

REM Install required packages from requirements.txt if available
if exist requirements.txt (
    echo Installing required packages...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install required packages.
        pause
        exit /b 1
    )
) else (
    echo requirements.txt not found. Ensure all dependencies are installed.
)

REM Construct the arguments string
set args=
:loop
if "%1"=="" goto endloop
set args=%args% %1
shift
goto loop
:endloop

REM Running the Python script with arguments
python autoReview.py %args%
if %errorlevel% neq 0 (
    echo Failed to run autoReview.py.
    pause
    exit /b 1
)