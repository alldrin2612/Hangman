# Hangman Game (Pygame Version)

A recreation of the web-based Hangman game using Pygame.

## Requirements

- Python 3.7+
- Pygame
- NumPy

## Quick Start

The easiest way to start is to run the setup script which will install dependencies and generate necessary assets:

```
cd "Hangman App"
python setup.py
```

After setup is complete, you can run the game:

```
python hangman_game.py
```

## Manual Installation

If you prefer to set up manually:

1. Install the required packages:
   ```
   cd "Hangman App"
   pip install -r requirements.txt
   ```

2. Download the Comic Neue font:
   ```
   python download_font.py
   ```

3. Generate sound files:
   ```
   python generate_sounds.py
   ```

4. Run the game:
   ```
   python hangman_game.py
   ```

## How to Play

1. Select a category from the menu screen.
2. Guess letters by clicking on the keyboard.
3. Try to guess the word before the hangman is complete!
4. You get 7 incorrect guesses before losing.

## Features

- Multiple word categories (Easy, Medium, Hard, Animals, Countries, Programming)
- Score tracking and high score
- Timer and best time tracking
- Sound effects
- Visual feedback on correct and incorrect guesses

## Controls

- Mouse: Select categories and letters
- Close button: Exit the game

## Custom Words

You can add your own words to the game by editing the `custom_words.txt` file. Each word should be on its own line.

## Troubleshooting

- If you encounter any font issues, make sure the Comic Neue Bold font is in the `fonts` directory.
- If sound doesn't work, check that the sound files exist in the `sounds` directory.
- For any other issues, try running `setup.py` again to reinstall dependencies and regenerate assets.

## Credits

Original web version created with Flask. Pygame version is a faithful recreation with the same features and design. 