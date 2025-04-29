from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
import time
import os
from custom_words import get_words, get_categories

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

@app.route('/')
def index():
    # Initialize session variables if not present
    if 'game_state' not in session:
        reset_game_session()
    
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset_game():
    reset_game_session()
    return jsonify({'status': 'success'})

@app.route('/select_category', methods=['POST'])
def select_category():
    category = request.json.get('category', 'MEDIUM')
    
    session['current_category'] = category
    session['word_list'] = get_words(category)
    session['word'] = random.choice(session['word_list'])
    session['guessed'] = []
    session['hangman_status'] = 0
    session['game_state'] = PLAYING
    session['start_time'] = time.time()
    
    return jsonify({
        'status': 'success',
        'word_length': len(session['word']),
        'category': category
    })

@app.route('/guess', methods=['POST'])
def make_guess():
    letter = request.json.get('letter', '').upper()
    
    if 'word' not in session or 'guessed' not in session:
        return jsonify({'status': 'error', 'message': 'Game not initialized'})
    
    if letter in session['guessed']:
        return jsonify({'status': 'error', 'message': 'Letter already guessed'})
    
    session['guessed'] = session['guessed'] + [letter]
    correct = letter in session['word']
    
    # Update hangman status for incorrect guesses
    if not correct:
        session['hangman_status'] = session['hangman_status'] + 1
    
    # Create display word with guessed letters revealed
    display_word = ""
    for char in session['word']:
        if char in session['guessed']:
            display_word += char
        else:
            display_word += "_"
    
    # Check win/lose conditions
    game_over = False
    won = "_" not in display_word
    lost = session['hangman_status'] >= 7
    
    if won or lost:
        session['game_state'] = GAME_OVER
        game_time = time.time() - session['start_time']
        
        if won:
            # Update score and best time
            session['score'] = session['score'] + 1
            if session['score'] > session['high_score']:
                session['high_score'] = session['score']
            
            if game_time < session['best_time'] or session['best_time'] == 0:
                session['best_time'] = game_time
        else:
            # Reset score on loss
            session['score'] = 0
        
        game_over = True
    
    return jsonify({
        'status': 'success',
        'correct': correct,
        'display_word': display_word,
        'hangman_status': session['hangman_status'],
        'game_over': game_over,
        'won': won,
        'word': session['word'] if game_over else None,
        'score': session['score'],
        'high_score': session['high_score'],
        'game_time': round(time.time() - session['start_time'], 1),
        'best_time': round(session['best_time'], 1) if session['best_time'] > 0 else 0
    })

@app.route('/get_categories')
def categories():
    return jsonify({'categories': get_categories()})

@app.route('/game_state')
def game_state():
    if 'game_state' not in session:
        reset_game_session()
    
    # Create display word with guessed letters revealed
    display_word = ""
    if 'word' in session:
        for char in session['word']:
            if char in session['guessed']:
                display_word += char
            else:
                display_word += "_"
    
    return jsonify({
        'game_state': session.get('game_state', MENU),
        'hangman_status': session.get('hangman_status', 0),
        'display_word': display_word,
        'guessed': session.get('guessed', []),
        'score': session.get('score', 0),
        'high_score': session.get('high_score', 0),
        'category': session.get('current_category', 'MEDIUM'),
        'best_time': round(session.get('best_time', 0), 1),
        'game_time': round(time.time() - session.get('start_time', time.time()), 1) if session.get('start_time') else 0
    })

def reset_game_session():
    session['game_state'] = MENU
    session['score'] = 0
    session['high_score'] = session.get('high_score', 0)
    session['best_time'] = session.get('best_time', 0)
    session['current_category'] = 'MEDIUM'
    if 'word_list' not in session:
        session['word_list'] = get_words('MEDIUM')
    session['hangman_status'] = 0
    session['guessed'] = []

if __name__ == '__main__':
    app.run(debug=True) 