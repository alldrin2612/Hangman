document.addEventListener('DOMContentLoaded', () => {
    // Game elements
    const menuScreen = document.getElementById('menu-screen');
    const gameScreen = document.getElementById('game-screen');
    const gameOverScreen = document.getElementById('game-over-screen');
    const categoryButtons = document.getElementById('category-buttons');
    const wordContainer = document.getElementById('word-container');
    const keyboard = document.getElementById('keyboard');
    const scoreElement = document.getElementById('score');
    const highScoreElement = document.getElementById('high-score');
    const gameTimeElement = document.getElementById('game-time');
    const bestTimeElement = document.getElementById('best-time');
    const categoryDisplay = document.getElementById('category-display');
    const resultMessage = document.getElementById('result-message');
    const revealedWord = document.getElementById('revealed-word');
    const finalScore = document.getElementById('final-score');
    const finalHighScore = document.getElementById('final-high-score');
    const finalTime = document.getElementById('final-time');
    const finalBestTime = document.getElementById('final-best-time');
    const playAgainBtn = document.getElementById('play-again-btn');
    const menuBtn = document.getElementById('menu-btn');
    const particleCanvas = document.getElementById('particle-canvas');
    
    // Game state
    let gameState = 0; // 0: menu, 1: playing, 2: game over
    let currentCategory = '';
    let guessedLetters = [];
    let hangmanStatus = 0;
    let score = 0;
    let highScore = 0;
    let gameTime = 0;
    let bestTime = 0;
    let gameTimer;
    
    // Hangman parts
    const hangmanParts = [
        document.getElementById('rope'),
        document.getElementById('head'),
        document.getElementById('body'),
        document.getElementById('left-arm'),
        document.getElementById('right-arm'),
        document.getElementById('left-leg'),
        document.getElementById('right-leg')
    ];
    
    const face = document.getElementById('face');
    
    // Particles system
    const ctx = particleCanvas.getContext('2d');
    particleCanvas.width = window.innerWidth;
    particleCanvas.height = window.innerHeight;
    let particles = [];
    
    // Initialize the game
    initialize();
    
    // Event listeners
    playAgainBtn.addEventListener('click', resetGame);
    menuBtn.addEventListener('click', showMenu);
    
    // Functions
    function initialize() {
        loadCategories();
        loadGameState();
        setupParticleSystem();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            particleCanvas.width = window.innerWidth;
            particleCanvas.height = window.innerHeight;
        });
        
        // Start the animation loop
        animationLoop();
    }
    
    function loadCategories() {
        fetch('/get_categories')
            .then(response => response.json())
            .then(data => {
                categoryButtons.innerHTML = '';
                
                data.categories.forEach(category => {
                    const button = document.createElement('button');
                    button.className = 'category-btn';
                    button.textContent = category;
                    button.addEventListener('click', () => selectCategory(category));
                    categoryButtons.appendChild(button);
                });
            })
            .catch(error => console.error('Error loading categories:', error));
    }
    
    function loadGameState() {
        fetch('/game_state')
            .then(response => response.json())
            .then(data => {
                gameState = data.game_state;
                hangmanStatus = data.hangman_status;
                guessedLetters = data.guessed;
                score = data.score;
                highScore = data.high_score;
                currentCategory = data.category;
                bestTime = data.best_time;
                gameTime = data.game_time;
                
                updateDisplay(data);
                updateHangman();
                
                // Show the appropriate screen
                if (gameState === 0) {
                    showMenu();
                } else if (gameState === 1) {
                    showGameScreen();
                    startTimer();
                } else if (gameState === 2) {
                    showGameOverScreen();
                }
            })
            .catch(error => console.error('Error loading game state:', error));
    }
    
    function selectCategory(category) {
        fetch('/select_category', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ category: category }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                currentCategory = data.category;
                createKeyboard();
                resetHangman();
                guessedLetters = [];
                showGameScreen();
                startTimer();
                
                // Update category display
                categoryDisplay.textContent = `Category: ${currentCategory}`;
                
                // Create word display
                updateWordDisplay('_'.repeat(data.word_length).split('').join(' '));
            }
        })
        .catch(error => console.error('Error selecting category:', error));
    }
    
    function makeGuess(letter) {
        if (guessedLetters.includes(letter)) return;
        
        fetch('/guess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ letter }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const keyElement = document.querySelector(`[data-key="${letter}"]`);
                
                if (data.correct) {
                    if (keyElement) {
                        keyElement.classList.add('correct');
                        keyElement.classList.add('disabled');
                        createParticles(keyElement.getBoundingClientRect());
                        playSound('correct');
                    }
                } else {
                    if (keyElement) {
                        keyElement.classList.add('incorrect');
                        keyElement.classList.add('disabled');
                        playSound('wrong');
                    }
                    
                    // Update hangman
                    hangmanStatus = data.hangman_status;
                    updateHangman();
                }
                
                // Update word display
                updateWordDisplay(data.display_word.split('').join(' '));
                
                // Update game stats
                scoreElement.textContent = data.score;
                highScoreElement.textContent = data.high_score;
                gameTimeElement.textContent = data.game_time;
                bestTimeElement.textContent = data.best_time;
                
                // Check game over
                if (data.game_over) {
                    stopTimer();
                    
                    // Update game over screen
                    finalScore.textContent = data.score;
                    finalHighScore.textContent = data.high_score;
                    finalTime.textContent = data.game_time;
                    finalBestTime.textContent = data.best_time;
                    revealedWord.textContent = data.word;
                    
                    if (data.won) {
                        resultMessage.textContent = "You Won!";
                        resultMessage.className = "won";
                        createVictoryParticles();
                        playSound('win');
                    } else {
                        resultMessage.textContent = "You Lost!";
                        resultMessage.className = "lost";
                        showFace();
                        playSound('lose');
                    }
                    
                    setTimeout(() => {
                        showGameOverScreen();
                    }, 1500);
                }
                
                // Update guessed letters
                guessedLetters.push(letter);
            }
        })
        .catch(error => console.error('Error making guess:', error));
    }
    
    function createKeyboard() {
        keyboard.innerHTML = '';
        const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        
        for (let i = 0; i < letters.length; i++) {
            const letter = letters[i];
            const key = document.createElement('button');
            key.className = 'keyboard-key';
            key.textContent = letter;
            key.dataset.key = letter;
            key.style.animationDelay = `${i * 30}ms`;
            
            key.addEventListener('click', () => makeGuess(letter));
            
            keyboard.appendChild(key);
        }
    }
    
    function updateWordDisplay(word) {
        wordContainer.textContent = word;
    }
    
    function updateDisplay(data) {
        if (data.display_word) {
            updateWordDisplay(data.display_word.split('').join(' '));
        }
        
        scoreElement.textContent = data.score;
        highScoreElement.textContent = data.high_score;
        gameTimeElement.textContent = data.game_time;
        bestTimeElement.textContent = data.best_time;
        categoryDisplay.textContent = `Category: ${data.category}`;
    }
    
    function updateHangman() {
        // Hide all parts first
        hangmanParts.forEach(part => {
            part.classList.remove('visible');
            part.classList.add('hidden');
        });
        
        // Show parts based on status
        for (let i = 0; i < hangmanStatus; i++) {
            if (i < hangmanParts.length) {
                hangmanParts[i].classList.remove('hidden');
                hangmanParts[i].classList.add('visible');
            }
        }
    }
    
    function resetHangman() {
        hangmanStatus = 0;
        updateHangman();
        face.classList.remove('visible');
        face.classList.add('hidden');
    }
    
    function showFace() {
        face.classList.remove('hidden');
        face.classList.add('visible');
    }
    
    function showMenu() {
        menuScreen.classList.remove('hidden');
        gameScreen.classList.add('hidden');
        gameOverScreen.classList.add('hidden');
        stopTimer();
        
        // Reset game state
        fetch('/reset', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            gameState = 0;
        })
        .catch(error => console.error('Error resetting game:', error));
    }
    
    function showGameScreen() {
        menuScreen.classList.add('hidden');
        gameScreen.classList.remove('hidden');
        gameOverScreen.classList.add('hidden');
    }
    
    function showGameOverScreen() {
        menuScreen.classList.add('hidden');
        gameScreen.classList.add('hidden');
        gameOverScreen.classList.remove('hidden');
    }
    
    function resetGame() {
        // Select the same category again to reset the game
        selectCategory(currentCategory);
    }
    
    function startTimer() {
        stopTimer();
        gameTimer = setInterval(() => {
            gameTime += 0.1;
            gameTimeElement.textContent = gameTime.toFixed(1);
        }, 100);
    }
    
    function stopTimer() {
        if (gameTimer) {
            clearInterval(gameTimer);
            gameTimer = null;
        }
    }
    
    // Particle system
    function setupParticleSystem() {
        particleCanvas.width = window.innerWidth;
        particleCanvas.height = window.innerHeight;
    }
    
    function createParticles(rect) {
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        for (let i = 0; i < 10; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = 1 + Math.random() * 3;
            const size = 2 + Math.random() * 4;
            const life = 30 + Math.random() * 30;
            const color = getRandomColor();
            
            particles.push({
                x: centerX,
                y: centerY,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                size,
                color,
                life,
                maxLife: life
            });
        }
    }
    
    function createVictoryParticles() {
        for (let i = 0; i < 100; i++) {
            const x = Math.random() * window.innerWidth;
            const y = Math.random() * window.innerHeight;
            const angle = Math.random() * Math.PI * 2;
            const speed = 1 + Math.random() * 5;
            const size = 3 + Math.random() * 5;
            const life = 60 + Math.random() * 60;
            const color = getRandomColor();
            
            particles.push({
                x,
                y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                size,
                color,
                life,
                maxLife: life
            });
        }
    }
    
    function updateParticles() {
        particles = particles.filter(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            particle.life -= 1;
            
            return particle.life > 0;
        });
    }
    
    function drawParticles() {
        ctx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);
        
        particles.forEach(particle => {
            const alpha = particle.life / particle.maxLife;
            ctx.globalAlpha = alpha;
            ctx.fillStyle = particle.color;
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fill();
        });
        
        ctx.globalAlpha = 1;
    }
    
    function animationLoop() {
        updateParticles();
        drawParticles();
        requestAnimationFrame(animationLoop);
    }
    
    function getRandomColor() {
        const colors = [
            '#ff7675', '#74b9ff', '#55efc4', '#ffeaa7', '#a29bfe',
            '#fd79a8', '#00cec9', '#fdcb6e', '#e17055', '#6c5ce7'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }
    
    // Sound functions
    function playSound(type) {
        const audio = new Audio(`/static/sounds/${type}.wav`);
        audio.play().catch(error => console.error('Error playing sound:', error));
    }
}); 