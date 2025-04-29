"""
Hangman Game - Main Launcher
Run this file to start the game.
"""

import os
import sys

# Set the current working directory to this script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Check if this is the first run
if not os.path.exists(os.path.join("fonts", "ComicNeue-Bold.ttf")) or \
   not os.path.exists(os.path.join("sounds", "win.wav")):
    print("First run detected. Setting up the game...")
    try:
        import setup
        setup.setup()
    except ImportError:
        print("Setup module not found. Please run setup.py manually.")
        sys.exit(1)

# Run the game
from hangman_game import HangmanGame

if __name__ == "__main__":
    game = HangmanGame()
    game.run() 