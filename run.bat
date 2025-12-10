@echo off
echo ================================================
echo Sir's ThisVid Scraper
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python from https://python.org/downloads
    echo Make sure to tick "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Checking dependencies...
pip install -r requirements.txt --quiet

REM Run the scraper
echo.
echo Starting scraper...
echo.
python scraper.py

echo.
echo ================================================
echo Done! Press any key to close.
pause >nul
