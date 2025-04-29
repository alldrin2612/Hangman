# Hangman Web Game

A modern, interactive web-based implementation of the classic Hangman word guessing game built with Flask.

![Hangman Game](/static/img/game_preview.png)

## Features

- Clean, responsive interface with animated elements
- Multiple word categories and difficulty levels (Easy, Medium, Hard)
- Themed word collections (Animals, Countries, Programming)
- Score tracking and personal best times
- Visual hangman progression with SVG graphics
- Victory/defeat animations with particle effects
- Custom sound effects
- Mobile-friendly design

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Dependencies**: 
  - Flask 2.3.3
  - Pygame 2.5.2 (for sound generation)
  - NumPy 1.26.0

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Hangman-Web.git
   cd Hangman-Web
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000/`

## How to Play

1. Start by selecting a difficulty category (Easy, Medium, Hard) or a themed word collection
2. Guess one letter at a time by clicking on the on-screen keyboard or using your physical keyboard
3. Try to guess the word before the hangman is complete (7 incorrect guesses)
4. Your score increases with each word you successfully guess
5. The game tracks your high score and best time

## Custom Word Lists

You can add your own words by editing the `custom_words.txt` file. Each line should contain a new word.

The game automatically loads words from this file into a "CUSTOM" category.

## Sound Effects

The game includes sound effects for correct guesses, incorrect guesses, winning, and losing. These sounds are generated using the `generate_web_sounds.py` script:

```
python generate_web_sounds.py
```

## Project Structure

- `app.py` - Main Flask application
- `custom_words.py` - Word lists and category management
- `custom_words.txt` - User-defined custom words
- `generate_web_sounds.py` - Sound effect generator
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, and sound files

## Screenshots

### Main Menu
![Main Menu](/static/img/menu.png)

### Gameplay
![Gameplay](/static/img/gameplay.png)

### Game Over
![Game Over](/static/img/gameover.png)

## License

[MIT License](LICENSE)

## Author

Your Name

## Acknowledgments

- Original Hangman game concept
- Flask web framework
- Contributors and testers
