# 🏆 Chess Game Analyzer for Windows

A web-based chess analysis tool that helps you improve your game by analyzing PGN files from Chess.com with AI-powered move suggestions.

## 🚀 Quick Start (2 Steps!)

### Step 1: Setup (One-time)
1. **Download Python**: Go to [python.org](https://www.python.org/downloads/) and install Python 3.11+
   - ⚠️ **Important**: Check "Add Python to PATH" during installation
2. **Download Stockfish**: Go to [stockfishchess.org](https://stockfishchess.org/download/) 
   - Download the Windows version and extract to `C:\stockfish\`
3. **Run Setup**: Double-click `setup_windows.bat` in the project folder

### Step 2: Use the Application
1. **Start**: Double-click `start_chess_analyzer.bat`
2. **Open Browser**: Go to `http://localhost:5000`
3. **Upload**: Drag your Chess.com PGN file to the web page
4. **Analyze**: Get AI-powered move suggestions and analysis!

## 📁 What You Need

### Files Included:
- `setup_windows.bat` - One-click setup script
- `start_chess_analyzer.bat` - One-click start script  
- `app.py` - Main application
- `templates/` - Web interface files
- `static/` - Styling and scripts
- `sample_game.pgn` - Example game to test

### Downloads Required:
- **Python 3.11+** from [python.org](https://www.python.org/downloads/)
- **Stockfish Engine** from [stockfishchess.org](https://stockfishchess.org/download/)

## 🎯 How to Get PGN Files from Chess.com

1. Go to any completed game on Chess.com
2. Click the "Analysis" tab
3. Click "Download PGN" button
4. Save the .pgn file to your computer
5. Upload it to the Chess Analyzer!

## 🔧 Troubleshooting

### Common Issues:

**"Python is not recognized"**
- Reinstall Python and check "Add Python to PATH"

**"Stockfish not found"**
- Download Stockfish and extract to `C:\stockfish\`
- Make sure you have `C:\stockfish\stockfish.exe`

**Application won't start**
- Run `test_windows.py` to check your setup
- Make sure antivirus isn't blocking the application

**Browser doesn't open automatically**
- Manually go to `http://localhost:5000`

## ✨ Features

- 🎮 **Easy Upload**: Drag-and-drop PGN files
- 🧠 **AI Analysis**: Stockfish-powered move suggestions  
- 📱 **Modern Interface**: Clean, responsive web design
- ⚡ **Real-time**: Instant analysis of any position
- 🎯 **Educational**: Learn from better move suggestions
- ♟️ **Interactive Chess Board**: Full chess board with pieces and coordinates
- 🎨 **Visual Move Suggestions**: Arrows and highlights show better moves
- 📊 **Move Quality**: Color-coded moves (excellent !, good, inaccuracy ?, blunder ??)
- ⌨️ **Keyboard Navigation**: Arrow keys to navigate through moves
- 🔍 **Click Analysis**: Click any move to get instant engine evaluation

## 🏅 System Requirements

- **OS**: Windows 10 or Windows 11
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 100MB free space
- **Browser**: Chrome, Firefox, Edge, or Safari

## 📞 Need Help?

1. **Run the test**: `python test_windows.py`
2. **Check setup**: Review `WINDOWS_SETUP.md` for detailed instructions
3. **Verify files**: Make sure all project files are in the same folder

---

**Ready to improve your chess game? Let's get started! ♟️🏆**