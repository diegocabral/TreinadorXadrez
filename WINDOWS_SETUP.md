# Chess Game Analyzer - Windows Setup Guide

## 🪟 Windows Installation Instructions

This guide will help you set up and run the Chess Game Analyzer on Windows 10/11.

## 📋 Prerequisites

Before starting, ensure you have:
- Windows 10 or Windows 11
- Administrator privileges for installing software
- Internet connection for downloading dependencies

## 🔧 Step-by-Step Installation

### Step 1: Install Python

1. **Download Python 3.11+**:
   - Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Click "Download Python 3.11.x" (or latest version)
   - **Important**: Check "Add Python to PATH" during installation

2. **Verify Python Installation**:
   ```cmd
   python --version
   pip --version
   ```

### Step 2: Install Stockfish Chess Engine

#### Option A: Download Stockfish Binary (Recommended)
1. **Download Stockfish**:
   - Go to [https://stockfishchess.org/download/](https://stockfishchess.org/download/)
   - Download "Windows" version (stockfish-windows-x86-64-avx2.zip)

2. **Extract and Install**:
   ```cmd
   # Create a directory for Stockfish
   mkdir C:\stockfish
   # Extract the downloaded zip to C:\stockfish\
   # You should have C:\stockfish\stockfish.exe
   ```

3. **Add to PATH** (Optional but recommended):
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Click "Environment Variables"
   - Under "System Variables", find "Path" and click "Edit"
   - Click "New" and add `C:\stockfish`
   - Click "OK" to save

#### Option B: Using Package Manager (Advanced)
```cmd
# If you have Chocolatey installed
choco install stockfish

# If you have Scoop installed
scoop install stockfish
```

### Step 3: Set Up the Project

1. **Create Project Directory**:
   ```cmd
   mkdir C:\chess-analyzer
   cd C:\chess-analyzer
   ```

2. **Create Virtual Environment**:
   ```cmd
   python -m venv venv
   ```

3. **Activate Virtual Environment**:
   ```cmd
   venv\Scripts\activate
   ```
   You should see `(venv)` at the beginning of your command prompt.

4. **Install Python Dependencies**:
   ```cmd
   pip install Flask==2.3.3 python-chess==1.999 Werkzeug==2.3.7 stockfish==3.28.0 requests
   ```

### Step 4: Download Project Files

Copy all the project files to `C:\chess-analyzer\`:
- `app.py`
- `requirements.txt` 
- `sample_game.pgn`
- `templates\` folder with HTML files
- `static\` folder with CSS and JS files

## 🚀 Running the Application

### Start the Application

1. **Open Command Prompt as Administrator**
2. **Navigate to project directory**:
   ```cmd
   cd C:\chess-analyzer
   ```

3. **Activate virtual environment**:
   ```cmd
   venv\Scripts\activate
   ```

4. **Start the application**:
   ```cmd
   python app.py
   ```

5. **Open your browser** and go to: `http://localhost:5000`

## 🔧 Windows-Specific Configuration

### Update app.py for Windows Stockfish Path

The application needs to be updated to find Stockfish on Windows. Here's the modified configuration:

```python
def get_stockfish_engine():
    """Initialize Stockfish engine with optimal settings for Windows"""
    try:
        # Windows-specific Stockfish paths
        stockfish_paths = [
            'C:\\stockfish\\stockfish.exe',
            'C:\\Program Files\\stockfish\\stockfish.exe',
            'stockfish.exe',  # if in PATH
            'stockfish',      # fallback
        ]
        
        for path in stockfish_paths:
            try:
                stockfish = Stockfish(path=path, depth=15, parameters={
                    "Threads": 2,
                    "Hash": 256,
                    "Skill Level": 20
                })
                # Test if the engine is working
                if stockfish.is_fen_valid("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
                    print(f"✅ Stockfish engine initialized successfully at: {path}")
                    return stockfish
            except Exception as e:
                print(f"Failed to initialize Stockfish at {path}: {e}")
                continue
        print("❌ Warning: Could not initialize Stockfish engine. Move analysis will be disabled.")
        return None
    except Exception as e:
        print(f"Error initializing Stockfish: {e}")
        return None
```

## 🧪 Testing on Windows

### Quick Test Script

Create `test_windows.py`:

```python
import os
import subprocess
import requests
import time

def test_windows_setup():
    print("🪟 Testing Chess Analyzer on Windows...")
    
    # Test Python
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
    except:
        print("❌ Python not found")
        return
    
    # Test Stockfish
    stockfish_paths = [
        'C:\\stockfish\\stockfish.exe',
        'stockfish.exe'
    ]
    
    stockfish_found = False
    for path in stockfish_paths:
        if os.path.exists(path) or subprocess.run(['where', 'stockfish'], capture_output=True).returncode == 0:
            print(f"✅ Stockfish found")
            stockfish_found = True
            break
    
    if not stockfish_found:
        print("❌ Stockfish not found. Please install it.")
    
    print("🎯 Setup test complete!")

if __name__ == "__main__":
    test_windows_setup()
```

### Run Test:
```cmd
python test_windows.py
```

## 🛠️ Troubleshooting Windows Issues

### Common Problems and Solutions

#### 1. **Python not found**
```cmd
# Check if Python is in PATH
where python
# If not found, reinstall Python with "Add to PATH" checked
```

#### 2. **Stockfish not found**
```cmd
# Verify Stockfish location
dir C:\stockfish\stockfish.exe
# Or check if it's in PATH
where stockfish
```

#### 3. **Virtual environment issues**
```cmd
# Delete and recreate virtual environment
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### 4. **Port already in use**
```cmd
# Find process using port 5000
netstat -ano | findstr :5000
# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

#### 5. **Permission errors**
- Run Command Prompt as Administrator
- Check Windows Defender/Antivirus settings
- Ensure project folder has write permissions

### Windows Firewall

If you get firewall warnings:
1. Click "Allow access" when prompted
2. Or manually add Python to Windows Firewall exceptions

## 📂 Windows File Structure

```
C:\chess-analyzer\
├── venv\                    # Virtual environment
├── app.py                   # Main application
├── requirements.txt         # Dependencies
├── sample_game.pgn         # Test file
├── templates\              # HTML templates
│   ├── base.html
│   ├── index.html
│   └── analysis.html
├── static\                 # Static files
│   ├── css\style.css
│   └── js\main.js
└── uploads\                # Auto-created for file uploads
```

## 🎯 Quick Start Commands

```cmd
# Setup (one-time)
mkdir C:\chess-analyzer
cd C:\chess-analyzer
python -m venv venv
venv\Scripts\activate
pip install Flask python-chess stockfish Werkzeug requests

# Run application
cd C:\chess-analyzer
venv\Scripts\activate
python app.py
```

## 🔄 Creating a Windows Batch File

Create `start_chess_analyzer.bat`:

```batch
@echo off
cd /d C:\chess-analyzer
call venv\Scripts\activate
python app.py
pause
```

Double-click this file to start the application easily!

## 🎉 Success!

Once everything is set up, you should see:
```
✅ Stockfish engine initialized successfully at: C:\stockfish\stockfish.exe
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

Open your browser to `http://localhost:5000` and start analyzing your chess games! 🏆♟️

## 💡 Pro Tips for Windows Users

1. **Use Windows Terminal** for better command line experience
2. **Pin the batch file** to taskbar for quick access
3. **Create a desktop shortcut** to the application URL
4. **Use Windows Subsystem for Linux (WSL)** if you prefer Linux commands
5. **Consider VS Code** for editing project files with syntax highlighting

Happy chess analyzing on Windows! 🪟🏆