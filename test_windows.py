#!/usr/bin/env python3
"""
Windows-specific test script for the Chess Game Analyzer
"""

import os
import subprocess
import sys
import time
import platform

def check_python():
    """Check Python installation and version"""
    try:
        version = sys.version_info
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} found")
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("⚠️  Warning: Python 3.8+ recommended")
        return True
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False

def check_pip():
    """Check if pip is available"""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ pip available: {result.stdout.strip()}")
            return True
        else:
            print("❌ pip not available")
            return False
    except Exception as e:
        print(f"❌ pip check failed: {e}")
        return False

def check_stockfish():
    """Check for Stockfish engine on Windows"""
    stockfish_paths = [
        'C:\\stockfish\\stockfish.exe',
        'C:\\Program Files\\stockfish\\stockfish.exe',
    ]
    
    # Check specific paths
    for path in stockfish_paths:
        if os.path.exists(path):
            print(f"✅ Stockfish found at: {path}")
            return True
    
    # Check if stockfish is in PATH
    try:
        result = subprocess.run(['where', 'stockfish'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Stockfish found in PATH: {result.stdout.strip()}")
            return True
    except:
        pass
    
    # Check for stockfish.exe in PATH
    try:
        result = subprocess.run(['where', 'stockfish.exe'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Stockfish.exe found in PATH: {result.stdout.strip()}")
            return True
    except:
        pass
    
    print("❌ Stockfish not found")
    print("💡 Install from: https://stockfishchess.org/download/")
    print("   Extract to C:\\stockfish\\ or add to PATH")
    return False

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'flask',
        'chess',
        'stockfish',
        'werkzeug'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} package available")
        except ImportError:
            print(f"❌ {package} package missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_virtual_environment():
    """Check if running in virtual environment"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
        return True
    else:
        print("⚠️  Not in virtual environment (recommended)")
        print("💡 Create with: python -m venv venv")
        print("   Activate with: venv\\Scripts\\activate")
        return False

def test_flask_import():
    """Test if Flask can be imported and basic functionality works"""
    try:
        from flask import Flask
        app = Flask(__name__)
        print("✅ Flask import successful")
        return True
    except Exception as e:
        print(f"❌ Flask import failed: {e}")
        return False

def test_chess_library():
    """Test python-chess library"""
    try:
        import chess
        import chess.pgn
        board = chess.Board()
        print("✅ python-chess library working")
        return True
    except Exception as e:
        print(f"❌ python-chess test failed: {e}")
        return False

def test_stockfish_integration():
    """Test Stockfish integration"""
    try:
        from stockfish import Stockfish
        
        # Try to initialize with common Windows paths
        stockfish_paths = [
            'C:\\stockfish\\stockfish.exe',
            'stockfish.exe',
            'stockfish'
        ]
        
        for path in stockfish_paths:
            try:
                stockfish = Stockfish(path=path)
                if stockfish.is_fen_valid("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
                    print(f"✅ Stockfish integration working with: {path}")
                    return True
            except:
                continue
        
        print("❌ Stockfish integration failed")
        print("💡 Make sure Stockfish is installed and accessible")
        return False
    except Exception as e:
        print(f"❌ Stockfish library test failed: {e}")
        return False

def check_file_structure():
    """Check if project files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'sample_game.pgn'
    ]
    
    required_dirs = [
        'templates',
        'static'
    ]
    
    all_present = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            all_present = False
    
    for dir in required_dirs:
        if os.path.exists(dir) and os.path.isdir(dir):
            print(f"✅ {dir}/ directory found")
        else:
            print(f"❌ {dir}/ directory missing")
            all_present = False
    
    return all_present

def main():
    """Run all Windows-specific tests"""
    print("🪟 Chess Game Analyzer - Windows Setup Test")
    print("=" * 50)
    
    print(f"\n🖥️  System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.architecture()[0]}")
    
    tests = [
        ("Python Installation", check_python),
        ("pip Availability", check_pip),
        ("Virtual Environment", check_virtual_environment),
        ("Project Files", check_file_structure),
        ("Python Dependencies", check_dependencies),
        ("Flask Import", test_flask_import),
        ("Chess Library", test_chess_library),
        ("Stockfish Engine", check_stockfish),
        ("Stockfish Integration", test_stockfish_integration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("🚀 Run: python app.py (or double-click start_chess_analyzer.bat)")
    elif passed >= total - 2:
        print("⚠️  Setup mostly ready. Check warnings above.")
        print("🚀 You can try running: python app.py")
    else:
        print("❌ Setup incomplete. Please address the failed tests.")
        print("📝 See WINDOWS_SETUP.md for detailed instructions.")
    
    print("\n💡 Tip: For best experience, install Stockfish for move analysis!")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")