@echo off
title Chess Game Analyzer
echo.
echo ♟️  Chess Game Analyzer - Starting...
echo.

REM Change to the project directory (update this path as needed)
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\" (
    echo ❌ Virtual environment not found!
    echo Please run setup first:
    echo    python -m venv venv
    echo    venv\Scripts\activate
    echo    pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ❌ Flask not found! Installing dependencies...
    pip install -r requirements.txt
)

REM Start the application
echo 🚀 Starting Chess Game Analyzer...
echo.
echo 📝 Instructions:
echo    1. Wait for "Running on http://127.0.0.1:5000" message
echo    2. Open your browser to: http://localhost:5000
echo    3. Upload a PGN file from Chess.com
echo    4. Press Ctrl+C here to stop the server
echo.

python app.py

echo.
echo 👋 Chess Game Analyzer stopped.
pause