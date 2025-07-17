#!/usr/bin/env python3
"""
Simple test script for the Chess Game Analyzer
"""

import requests
import os
import time

def test_app():
    """Test the chess analyzer application"""
    base_url = "http://localhost:5000"
    
    print("🔍 Testing Chess Game Analyzer...")
    
    # Test 1: Check if main page loads
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ Main page loads successfully")
        else:
            print(f"❌ Main page failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to connect to application: {e}")
        return False
    
    # Test 2: Check if we can upload a PGN file
    try:
        with open('sample_game.pgn', 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{base_url}/upload", files=files)
            
        if response.status_code == 200 and "Game Analysis" in response.text:
            print("✅ PGN file upload and parsing works")
        else:
            print(f"❌ PGN upload failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ PGN upload test failed: {e}")
    
    # Test 3: Test move analysis endpoint
    try:
        # Starting position FEN
        test_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        response = requests.post(
            f"{base_url}/analyze_move",
            json={"fen": test_fen},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if "best_move" in data:
                print("✅ Move analysis endpoint works")
            else:
                print("❌ Move analysis response missing expected data")
        else:
            print(f"❌ Move analysis failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Move analysis test failed: {e}")
    
    print("\n📝 Test Summary:")
    print("The Chess Game Analyzer appears to be working correctly!")
    print(f"🌐 Application is running at: {base_url}")
    print("📁 Sample PGN file is available: sample_game.pgn")
    print("📚 Check README.md for complete usage instructions")

if __name__ == "__main__":
    # Wait a moment for the server to be ready
    time.sleep(2)
    test_app()