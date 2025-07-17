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
            # Linux/Unix paths (most common first)
            '/usr/games/stockfish',
            '/usr/bin/stockfish',
            '/usr/local/bin/stockfish',
            '/opt/homebrew/bin/stockfish',
            'stockfish',
            # Windows paths
            'C:\\stockfish\\stockfish.exe',
            'C:\\Program Files\\stockfish\\stockfish.exe',
            'stockfish.exe'
        ]
        
        for path in stockfish_paths:
            try:
                stockfish = Stockfish(path=path, depth=12, parameters={
                    "Threads": 4,
                    "Hash": 512,
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
        
        # Format evaluation for display
        evaluation_text = ""
        if evaluation:
            if evaluation.get('type') == 'cp':
                centipawns = evaluation.get('value', 0)
                evaluation_text = f"{centipawns/100:+.2f} pawns"
            elif evaluation.get('type') == 'mate':
                mate_in = evaluation.get('value', 0)
                evaluation_text = f"Mate in {abs(mate_in)}"
        
        return {
            'best_move': best_move,
            'evaluation': evaluation_text or 'Unknown',
            'raw_evaluation': evaluation,
            'top_moves': top_moves or [],
            'move_quality': assess_move_quality(evaluation, top_moves)
        }
    except Exception as e:
        print(f"Error analyzing position: {e}")
        return None

def assess_move_quality(evaluation, top_moves):
    """Assess the quality of moves based on evaluation differences"""
    if not evaluation or not top_moves:
        return 'unknown'
    
    # This is a simplified move quality assessment
    # In practice, you'd compare with the position after the actual move
    if evaluation.get('type') == 'mate':
        return 'excellent'
    
    if evaluation.get('type') == 'cp':
        centipawns = abs(evaluation.get('value', 0))
        if centipawns <= 10:
            return 'excellent'
        elif centipawns <= 50:
            return 'good'
        elif centipawns <= 100:
            return 'inaccuracy'
        elif centipawns <= 300:
            return 'mistake'
        else:
            return 'blunder'
    
    return 'good'

def analyze_all_moves_automatically(game_data, stockfish):
    """Automatically analyze all moves in the game like Chess.com"""
    total_moves = len(game_data['moves'])
    print(f"📊 Auto-analyzing {total_moves} moves with optimized settings...")
    
    analyzed_moves = []
    board = chess.Board()
    
    # Reduce depth for auto-analysis to speed up processing
    original_depth = stockfish.depth
    stockfish.depth = 10  # Faster analysis for auto-mode
    
    for i, move_data in enumerate(game_data['moves']):
        try:
            # Analyze position before the move
            analysis = analyze_position(move_data['fen_before'], stockfish)
            
            # Create move object to check if it's in legal moves
            move = chess.Move.from_uci(move_data['uci'])
            
            # Determine move quality by comparing with engine suggestions
            move_quality = 'unknown'
            is_best = False
            is_good = False
            better_move = None
            
            if analysis and analysis.get('best_move') and analysis.get('top_moves'):
                best_move = analysis['best_move']
                top_moves = analysis.get('top_moves', [])
                
                # Debug info
                print(f"Move {i+1}: {move_data['san']} ({move_data['uci']}) vs Best: {best_move}")
                
                # Check if the played move is the best move (exact match)
                if move_data['uci'] == best_move:
                    move_quality = 'excellent'
                    is_best = True
                    print(f"  -> Excellent move (best)")
                else:
                    # Check if move is in top moves
                    move_found = False
                    for idx, top_move in enumerate(top_moves):
                        move_uci = top_move.get('Move', '')
                        if move_uci == move_data['uci']:
                            move_found = True
                            if idx == 0:  # Second best move
                                move_quality = 'good'
                                is_good = True
                                print(f"  -> Good move (rank {idx+1})")
                            elif idx <= 2:  # Top 3 moves
                                move_quality = 'inaccuracy'
                                print(f"  -> Inaccuracy (rank {idx+1})")
                            else:
                                move_quality = 'mistake'
                                print(f"  -> Mistake (rank {idx+1})")
                            break
                    
                    if not move_found:
                        # Move not in top 5, check evaluation difference
                        # Set position after the played move to compare evaluations
                        temp_board = chess.Board(move_data['fen_before'])
                        temp_board.push(move)
                        stockfish.set_fen_position(temp_board.fen())
                        after_eval = stockfish.get_evaluation()
                        
                        # Set position for best move to compare
                        temp_board2 = chess.Board(move_data['fen_before'])
                        best_move_obj = chess.Move.from_uci(best_move)
                        temp_board2.push(best_move_obj)
                        stockfish.set_fen_position(temp_board2.fen())
                        best_eval = stockfish.get_evaluation()
                        
                        # Compare evaluations to determine severity
                        eval_diff = calculate_evaluation_difference(after_eval, best_eval)
                        
                        if eval_diff >= 300:  # 3+ pawns worse
                            move_quality = 'blunder'
                            print(f"  -> Blunder (eval diff: {eval_diff})")
                        elif eval_diff >= 100:  # 1+ pawns worse
                            move_quality = 'mistake'
                            print(f"  -> Mistake (eval diff: {eval_diff})")
                        else:
                            move_quality = 'inaccuracy'
                            print(f"  -> Inaccuracy (eval diff: {eval_diff})")
                        
                        better_move = best_move
                    elif not is_good and not is_best:
                        better_move = best_move
            else:
                print(f"  -> No analysis available")
            
            # Add analysis data to move
            enhanced_move = move_data.copy()
            enhanced_move['analysis'] = analysis
            enhanced_move['move_quality'] = move_quality
            enhanced_move['is_best'] = is_best
            enhanced_move['is_good'] = is_good
            enhanced_move['better_move'] = better_move
            
            analyzed_moves.append(enhanced_move)
            
            # Make the move on the board for next iteration
            board.push(move)
            
            # Progress indicator (more frequent for user feedback)
            if (i + 1) % 3 == 0 or i == total_moves - 1:
                progress = int((i + 1) / total_moves * 100)
                print(f"⏳ Progress: {i + 1}/{total_moves} moves ({progress}%)")
                
        except Exception as e:
            print(f"❌ Error analyzing move {i + 1}: {e}")
            # Add move without analysis
            enhanced_move = move_data.copy()
            enhanced_move['analysis'] = None
            enhanced_move['move_quality'] = 'unknown'
            enhanced_move['is_best'] = False
            enhanced_move['is_good'] = False
            enhanced_move['better_move'] = None
            analyzed_moves.append(enhanced_move)
            
            try:
                board.push(chess.Move.from_uci(move_data['uci']))
            except:
                pass
    
    # Restore original depth
    stockfish.depth = original_depth
    
    print("✅ Auto-analysis complete! Game ready for review.")
    
    # Calculate statistics
    excellent_moves = sum(1 for move in analyzed_moves if move['move_quality'] == 'excellent')
    good_moves = sum(1 for move in analyzed_moves if move['move_quality'] == 'good')
    inaccuracies = sum(1 for move in analyzed_moves if move['move_quality'] == 'inaccuracy')
    mistakes = sum(1 for move in analyzed_moves if move['move_quality'] == 'mistake')
    blunders = sum(1 for move in analyzed_moves if move['move_quality'] == 'blunder')
    
    print(f"📈 Game Statistics: {excellent_moves} excellent, {good_moves} good, {inaccuracies} inaccuracies, {mistakes} mistakes, {blunders} blunders")

    # Update game data
    game_data['moves'] = analyzed_moves
    game_data['auto_analyzed'] = True
    game_data['statistics'] = {
        'excellent': excellent_moves,
        'good': good_moves,
        'inaccuracies': inaccuracies,
        'mistakes': mistakes,
        'blunders': blunders
    }
    
    # Add debug information
    game_data['debug_info'] = f"Analyzed {len(analyzed_moves)} moves, Stats: {excellent_moves}E {good_moves}G {inaccuracies}I {mistakes}M {blunders}B"
    
    return game_data

def calculate_evaluation_difference(eval1, eval2):
    """Calculate the difference between two evaluations in centipawns"""
    if not eval1 or not eval2:
        return 0
    
    # Handle mate evaluations
    if eval1.get('type') == 'mate' or eval2.get('type') == 'mate':
        return 1000  # Large difference for mate scenarios
    
    # Handle centipawn evaluations
    if eval1.get('type') == 'cp' and eval2.get('type') == 'cp':
        return abs(eval1.get('value', 0) - eval2.get('value', 0))
    
    return 0

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
        
        # Automatically analyze all moves if Stockfish is available
        stockfish = get_stockfish_engine()
        if stockfish:
            print("🔍 Auto-analyzing game moves...")
            print(f"📋 Game has {len(game_data.get('moves', []))} moves to analyze")
            game_data = analyze_all_moves_automatically(game_data, stockfish)
            print(f"📊 Analysis complete. Statistics: {game_data.get('statistics', 'None')}")
        else:
            print("⚠️ Stockfish not available - skipping auto-analysis")
            print("💡 Install Stockfish to enable automatic move analysis")
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return render_template('analysis.html', game_data=game_data)
    else:
        flash('Please upload a valid PGN file')
        return redirect(url_for('index'))

@app.route('/analyze_position', methods=['POST'])
def analyze_position_route():
    """Analyze a specific position and return suggestions"""
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400
            
        fen = data.get('fen')
        
        if not fen:
            return jsonify({'success': False, 'error': 'No FEN position provided'}), 400
        
        stockfish = get_stockfish_engine()
        if not stockfish:
            return jsonify({'success': False, 'error': 'Chess engine not available. Please install Stockfish.'}), 500
        
        analysis = analyze_position(fen, stockfish)
        
        if not analysis:
            return jsonify({'success': False, 'error': 'Failed to analyze position'}), 500
        
        return jsonify({'success': True, 'analysis': analysis})
        
    except Exception as e:
        print(f"Error in analyze_position_route: {e}")
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

@app.route('/convert_move', methods=['POST'])
def convert_move():
    """Convert UCI move to readable algebraic notation"""
    data = request.json
    fen = data.get('fen')
    uci_move = data.get('uci_move')
    
    if not fen or not uci_move:
        return jsonify({'error': 'Missing FEN or UCI move'}), 400
    
    try:
        board = chess.Board(fen)
        move = chess.Move.from_uci(uci_move)
        
        if move in board.legal_moves:
            san_move = board.san(move)
            return jsonify({'san_move': san_move})
        else:
            return jsonify({'error': 'Invalid move'}), 400
    except Exception as e:
        return jsonify({'error': f'Error converting move: {e}'}), 500

@app.route('/analyze_all/<game_id>')
def analyze_all_moves_route(game_id):
    """Redirect to perform auto-analysis on the current game"""
    # For now, just redirect back to the analysis page
    # In a real implementation, you might trigger re-analysis here
    return redirect(url_for('analyze_game', filename=game_id))

@app.route('/full_analysis/<int:game_id>')
def full_analysis(game_id):
    """Perform full game analysis (placeholder for future enhancement)"""
    return render_template('full_analysis.html', game_id=game_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)