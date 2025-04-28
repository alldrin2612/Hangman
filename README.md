# Hangman Web App

A modern web-based implementation of the classic Hangman word guessing game using Flask and JavaScript.

## Features

- Clean, responsive web interface with animations
- Particle effects when clicking letters
- Score tracking system
- Timer to track how fast you can guess words
- Best time tracking
- Sound effects for correct/incorrect guesses
- Multiple difficulty levels (Easy, Medium, Hard)
- Themed word categories (Animals, Countries, Programming)
- Custom word list support
- SVG-based hangman drawing with smooth transitions

## Requirements

- Python 3.6+
- Flask 2.3+
- NumPy 1.26.0+ (for sound generation)

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/hangman-web.git
cd hangman-web
```

2. Install required packages:
```
pip install -r requirements.txt
```

3. Generate sound files:
```
python generate_web_sounds.py
```

## Running the Web App

1. Start the Flask server:
```
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## How to Play

1. When you first open the app, you'll be presented with a category selection screen.
   
2. Select a Word Category:
   - Easy: Shorter words (4-6 letters)
   - Medium: Average length words (7-9 letters)
   - Hard: Longer, more challenging words (10+ letters)
   - Animals: Animal-themed words
   - Countries: Country names
   - Programming: Programming-related terms
   - Custom: Your own custom words (if available)

3. Game Rules:
   - You need to guess the hidden word by clicking on letter buttons
   - Each incorrect guess adds a part to the hangman
   - You lose if the hangman is completed (6 incorrect guesses)
   - You win if you guess the word before the hangman is complete

4. Features:
   - Your score increases with each win and resets on loss
   - The game tracks your best time for successful word guesses
   - Click the "Play Again" button at the end of each round to continue
   - Click the "Menu" button to return to category selection

## Project Structure

- `app.py` - The Flask server and game logic
- `custom_words.py` - Word lists and category management
- `generate_web_sounds.py` - Script to generate sound effects
- `templates/` - HTML templates
  - `index.html` - The main game interface
- `static/` - Static assets
  - `css/styles.css` - Game styling
  - `js/hangman.js` - Frontend game logic
  - `sounds/` - Game sound effects

## Customization

### Adding Custom Words

To add custom words, you can modify the `custom_words.py` file directly or use the original pygame-based word editor if available.

### Modifying Styles

The game's appearance can be customized by editing the `static/css/styles.css` file.

## Browser Compatibility

This web app has been tested and works well on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

This project is licensed under the MIT License - see the LICENSE file for details. 