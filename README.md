# Chess Game Analyzer

A comprehensive Python web-based system for analyzing chess games from PGN files. Upload your games from Chess.com and get AI-powered analysis with better move suggestions using the Stockfish engine.

## Features

- **PGN File Upload**: Easy drag-and-drop interface for uploading PGN files from Chess.com
- **Game Analysis**: Powered by Stockfish chess engine for professional-level analysis
- **Move-by-Move Analysis**: Click on any move to get detailed analysis and alternative suggestions
- **Interactive Interface**: Navigate through games with intuitive controls
- **Beautiful UI**: Modern, responsive design with chess-themed styling
- **Real-time Analysis**: Get instant feedback on chess positions
- **Multiple Move Suggestions**: See top 5 alternative moves with evaluations

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Chess Engine**: Stockfish 16
- **Chess Library**: python-chess for PGN parsing and position analysis
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Icons**: Font Awesome
- **File Handling**: Secure file uploads with validation

## Installation

### Prerequisites

- Python 3.8+ (Python 3.11+ recommended)
- Stockfish chess engine
- Windows 10/11, Linux, or macOS

### Quick Setup for Windows 🪟

1. **Download and extract all project files**
2. **Double-click `setup_windows.bat`** - This will:
   - Check Python installation
   - Create virtual environment
   - Install all dependencies
   - Check for Stockfish engine
3. **Double-click `start_chess_analyzer.bat`** to run the application
4. **Open browser to `http://localhost:5000`**

📝 **For detailed Windows instructions, see [WINDOWS_SETUP.md](WINDOWS_SETUP.md)**

### Manual Setup (All Platforms)

#### For Windows:
```cmd
# 1. Install Python from https://www.python.org/downloads/
# 2. Download Stockfish from https://stockfishchess.org/download/
# 3. Extract Stockfish to C:\stockfish\

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### For Linux/Ubuntu:
```bash
sudo apt update
sudo apt install python3-venv stockfish -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### For macOS:
```bash
brew install stockfish
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Then open your browser to: `http://localhost:5000`**

## Usage

### Getting Your PGN File from Chess.com

1. Go to your completed game on Chess.com
2. Click on the "Analysis" tab
3. Click the "Download PGN" button
4. Save the .pgn file to your computer

### Using the Analyzer

1. **Upload**: Drag and drop your PGN file or click to browse
2. **Analyze**: The system will automatically parse your game and display it
3. **Navigate**: Use the control buttons to move through the game
4. **Get Suggestions**: Click the search icon next to any move for detailed analysis
5. **Review**: See the best moves, evaluations, and alternative suggestions

### Analysis Features

- **Position Evaluation**: Get numerical evaluation of positions (in pawns or mate scores)
- **Best Move Suggestions**: See the engine's recommended best move
- **Alternative Moves**: View top 5 alternative moves with their evaluations
- **Move Navigation**: Step through the game move by move
- **Game Information**: View player names, ratings, date, and game result

## File Structure

```
chess-analyzer/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── sample_game.pgn       # Example PGN file for testing
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Upload page
│   └── analysis.html     # Game analysis page
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── main.js       # JavaScript utilities
├── uploads/              # Temporary file uploads (auto-created)
└── venv/                 # Virtual environment (auto-created)
```

## API Endpoints

- `GET /` - Main upload page
- `POST /upload` - Handle PGN file upload and parse game
- `POST /analyze_move` - Analyze specific chess position
- `GET /full_analysis/<int:game_id>` - Full game analysis (future feature)

## Configuration

The application includes several configurable settings in `app.py`:

- **Upload folder**: Where temporary files are stored
- **Max file size**: 16MB limit for PGN files
- **Stockfish depth**: Analysis depth (currently set to 15)
- **Engine parameters**: Threads, hash size, skill level

## Troubleshooting

### Common Issues

1. **Stockfish not found**:
   - Ensure Stockfish is installed: `sudo apt install stockfish`
   - Check if stockfish is in PATH: `which stockfish`

2. **Python dependencies issues**:
   - Make sure you're in the virtual environment: `source venv/bin/activate`
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **File upload errors**:
   - Check file format (must be .pgn)
   - Ensure file size is under 16MB
   - Verify PGN file is valid

4. **Analysis not working**:
   - Check if Stockfish engine is properly initialized
   - Look at console logs for error messages

### Getting Help

If you encounter issues:

1. Check the console output for error messages
2. Verify all dependencies are installed correctly
3. Ensure PGN file is properly formatted
4. Try the included `sample_game.pgn` for testing

## Future Enhancements

- **Full Game Analysis**: Automatically analyze entire games and highlight blunders
- **Opening Database**: Identify chess openings and provide information
- **Game Statistics**: Show accuracy percentages and move quality statistics
- **Export Features**: Save analysis results to files
- **Multi-game Support**: Analyze multiple games from a single PGN file
- **User Accounts**: Save and track analysis history
- **Chess Board Visualization**: Interactive chess board display
- **Engine Comparison**: Compare analysis from different chess engines

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit issues and enhancement requests.

---

**Happy analyzing! 🏆♟️**
