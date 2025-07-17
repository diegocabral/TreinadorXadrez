@echo off
title Chess Game Analyzer - Windows Setup
color 0A

echo.
echo ♟️ ===============================================
echo    Chess Game Analyzer - Windows Setup
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo ✅ Python found:
python --version

REM Create project directory if it doesn't exist
if not exist "venv\" (
    echo.
    echo 🔧 Creating virtual environment...
    python -m venv venv
    
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment!
        echo Make sure you have python-venv installed.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install --upgrade pip
pip install Flask==2.3.3 python-chess==1.999 Werkzeug==2.3.7 stockfish==3.28.0 requests

if errorlevel 1 (
    echo ❌ Failed to install Python dependencies!
    pause
    exit /b 1
)

REM Check for Stockfish
echo.
echo 🔍 Checking for Stockfish engine...

set STOCKFISH_FOUND=0

REM Check common Stockfish locations
if exist "C:\stockfish\stockfish.exe" (
    echo ✅ Stockfish found at: C:\stockfish\stockfish.exe
    set STOCKFISH_FOUND=1
) else (
    where stockfish >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Stockfish found in PATH
        set STOCKFISH_FOUND=1
    )
)

if %STOCKFISH_FOUND%==0 (
    echo.
    echo ⚠️  Stockfish chess engine not found!
    echo.
    echo To enable move analysis, please:
    echo 1. Download Stockfish from: https://stockfishchess.org/download/
    echo 2. Extract to C:\stockfish\ (so you have C:\stockfish\stockfish.exe)
    echo 3. Or add Stockfish to your system PATH
    echo.
    echo The application will still work for viewing games without analysis.
)

REM Create uploads directory
if not exist "uploads\" (
    mkdir uploads
)

echo.
echo ✅ Setup completed successfully!
echo.
echo 📝 Next steps:
echo 1. Double-click "start_chess_analyzer.bat" to run the application
echo 2. Or run manually with: python app.py
echo 3. Open browser to: http://localhost:5000
echo.

if %STOCKFISH_FOUND%==0 (
    echo ⚠️  Remember to install Stockfish for move analysis!
    echo.
)

echo 🎯 Ready to analyze your chess games!
pause