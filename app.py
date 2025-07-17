import os
import chess
import chess.pgn
import chess.engine
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import io
from stockfish import Stockfish

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Stockfish engine
def get_stockfish_engine():
    """Initialize Stockfish engine with optimal settings for Windows and Linux"""
    try:
        # Try common Stockfish paths for Windows and Linux
        stockfish_paths = [
            # Windows paths
            'C:\\stockfish\\stockfish.exe',
            'C:\\Program Files\\stockfish\\stockfish.exe',
            'stockfish.exe',
            # Linux/Unix paths
            '/usr/bin/stockfish',
            '/usr/local/bin/stockfish',
            '/opt/homebrew/bin/stockfish',
            'stockfish'
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
        print("💡 Please install Stockfish:")
        print("   Windows: Download from https://stockfishchess.org/download/")
        print("   Linux: sudo apt install stockfish")
        return None
    except Exception as e:
        print(f"Error initializing Stockfish: {e}")
        return None

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pgn'

def analyze_position(fen, stockfish=None):
    """Analyze a chess position and return best moves with evaluation"""
    if not stockfish:
        return None
    
    try:
        stockfish.set_fen_position(fen)
        
        # Get the best move
        best_move = stockfish.get_best_move()
        
        # Get evaluation
        evaluation = stockfish.get_evaluation()
        
        # Get top moves
        top_moves = stockfish.get_top_moves(5)
        
        return {
            'best_move': best_move,
            'evaluation': evaluation,
            'top_moves': top_moves
        }
    except Exception as e:
        print(f"Error analyzing position: {e}")
        return None

def parse_pgn_file(file_path):
    """Parse PGN file and extract game information"""
    try:
        with open(file_path, 'r') as pgn_file:
            game = chess.pgn.read_game(pgn_file)
            
        if not game:
            return None
            
        # Extract game metadata
        headers = dict(game.headers)
        
        # Get all moves
        moves = []
        board = game.board()
        
        for move_num, move in enumerate(game.mainline_moves()):
            # Store position before move
            fen_before = board.fen()
            san_move = board.san(move)
            
            # Make the move
            board.push(move)
            fen_after = board.fen()
            
            moves.append({
                'move_number': move_num + 1,
                'san': san_move,
                'uci': move.uci(),
                'fen_before': fen_before,
                'fen_after': fen_after,
                'white_move': move_num % 2 == 0
            })
        
        return {
            'headers': headers,
            'moves': moves,
            'final_fen': board.fen(),
            'result': headers.get('Result', '*')
        }
    except Exception as e:
        print(f"Error parsing PGN: {e}")
        return None

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle PGN file upload"""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Parse the PGN file
        game_data = parse_pgn_file(file_path)
        
        if not game_data:
            flash('Error parsing PGN file')
            return redirect(url_for('index'))
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return render_template('analysis.html', game_data=game_data)
    else:
        flash('Please upload a valid PGN file')
        return redirect(url_for('index'))

@app.route('/analyze_move', methods=['POST'])
def analyze_move():
    """Analyze a specific move and return suggestions"""
    data = request.json
    fen = data.get('fen')
    
    if not fen:
        return jsonify({'error': 'No FEN position provided'}), 400
    
    stockfish = get_stockfish_engine()
    if not stockfish:
        return jsonify({'error': 'Chess engine not available'}), 500
    
    analysis = analyze_position(fen, stockfish)
    
    if not analysis:
        return jsonify({'error': 'Failed to analyze position'}), 500
    
    return jsonify(analysis)

@app.route('/full_analysis/<int:game_id>')
def full_analysis(game_id):
    """Perform full game analysis (placeholder for future enhancement)"""
    return render_template('full_analysis.html', game_id=game_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)