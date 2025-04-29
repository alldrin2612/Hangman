import pygame
import sys
import random
import time
import os
from custom_words import get_words, get_categories

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
FPS = 60

# Colors
PRIMARY_COLOR = (23, 62, 67)  # #173e43
SECONDARY_COLOR = (63, 176, 172)  # #3fb0ac
ACCENT_COLOR = (250, 229, 150)  # #fae596
LIGHT_COLOR = (221, 223, 212)  # #dddfd4
DARK_COLOR = (23, 62, 67)  # #173e43
SUCCESS_COLOR = (76, 175, 80)  # #4caf50
ERROR_COLOR = (231, 76, 60)  # #e74c3c
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Fonts
def get_font(size):
    # Try to load the custom font if it exists
    font_path = os.path.join("fonts", "ComicNeue-Bold.ttf")
    if os.path.exists(font_path):
        return pygame.font.Font(font_path, size)
    else:
        # Use default pygame font if custom font is not available
        return pygame.font.SysFont("arial", size)

# Create a dummy sound object
class DummySound:
    def play(self):
        pass

# Load sounds
def load_sounds():
    sounds = {}
    sound_files = ["correct", "wrong", "win", "lose"]
    
    # Create empty sounds if files don't exist or have errors
    for sound in sound_files:
        sound_path = os.path.join("sounds", f"{sound}.wav")
        try:
            if os.path.exists(sound_path):
                sounds[sound] = pygame.mixer.Sound(sound_path)
            else:
                sounds[sound] = DummySound()
        except:
            # If there's any error loading the sound, use a dummy sound
            sounds[sound] = DummySound()
            print(f"Could not load sound: {sound_path}")
    
    return sounds

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, font_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = get_font(font_size)
        self.is_hovered = False
        self.is_disabled = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered and not self.is_disabled else self.color
        if self.is_disabled:
            color = (204, 204, 204)  # Grey for disabled buttons
        
        # Draw button background
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        
        # Draw button text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        if not self.is_disabled:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and not self.is_disabled:
                return True
        return False

class KeyboardKey(Button):
    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height, text, SECONDARY_COLOR, PRIMARY_COLOR, WHITE, 24)
        self.original_color = self.color
        self.status = "normal"  # "normal", "correct", "incorrect"

    def set_status(self, status):
        self.status = status
        if status == "normal":
            self.color = self.original_color
            self.is_disabled = False
        elif status == "correct":
            self.color = SUCCESS_COLOR
            self.is_disabled = True
        elif status == "incorrect":
            self.color = ERROR_COLOR
            self.is_disabled = True

class HangmanGame:
    def __init__(self):
        # Set up the game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hangman Game")
        self.clock = pygame.time.Clock()
        
        # Create fonts directory
        os.makedirs("fonts", exist_ok=True)
        os.makedirs("sounds", exist_ok=True)
        
        # Game state
        self.game_state = MENU
        self.score = 0
        self.high_score = 0
        self.best_time = 0
        self.start_time = 0
        self.end_time = 0  # Track when the game ends
        self.current_category = "MEDIUM"
        self.word = ""
        self.guessed = []
        self.hangman_status = 0
        self.word_list = get_words("MEDIUM")
        
        # Create the game elements
        self.create_category_buttons()
        self.create_keyboard()
        self.create_game_buttons()
        
        # Load sounds
        try:
            self.sounds = load_sounds()
        except Exception as e:
            print(f"Error loading sounds: {e}")
            # Create dummy sounds as fallback
            self.sounds = {
                "correct": DummySound(),
                "wrong": DummySound(),
                "win": DummySound(),
                "lose": DummySound()
            }

    def create_category_buttons(self):
        self.category_buttons = []
        categories = get_categories()
        x_start = (SCREEN_WIDTH - (200 * 3 + 30)) // 2
        y_start = 150
        
        for i, category in enumerate(categories):
            row = i // 3
            col = i % 3
            x = x_start + col * (200 + 15)
            y = y_start + row * (60 + 15)
            
            button = Button(x, y, 200, 60, category, SECONDARY_COLOR, PRIMARY_COLOR, WHITE, 24)
            self.category_buttons.append((category, button))

    def create_keyboard(self):
        self.keyboard = {}
        keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key_width, key_height = 45, 45
        x_start = (SCREEN_WIDTH - (key_width * 10 + 10 * 9)) // 2
        y_start = 450
        
        for i, key in enumerate(keys):
            row = i // 10
            col = i % 10
            x = x_start + col * (key_width + 10)
            y = y_start + row * (key_height + 10)
            
            self.keyboard[key] = KeyboardKey(x, y, key_width, key_height, key)

    def create_game_buttons(self):
        # Play again button
        self.play_again_btn = Button(
            SCREEN_WIDTH // 2 - 120, 
            SCREEN_HEIGHT - 120,
            110, 50, 
            "Play Again", 
            SECONDARY_COLOR, 
            PRIMARY_COLOR, 
            WHITE, 
            22
        )
        
        # Menu button
        self.menu_btn = Button(
            SCREEN_WIDTH // 2 + 10, 
            SCREEN_HEIGHT - 120,
            110, 50, 
            "Menu", 
            SECONDARY_COLOR, 
            PRIMARY_COLOR, 
            WHITE, 
            22
        )

    def reset_game(self):
        self.guessed = []
        self.hangman_status = 0
        for key in self.keyboard:
            self.keyboard[key].set_status("normal")

    def select_category(self, category):
        self.current_category = category
        self.word_list = get_words(category)
        self.word = random.choice(self.word_list)
        self.guessed = []
        self.hangman_status = 0
        self.game_state = PLAYING
        self.start_time = time.time()
        
        # Reset keyboard
        for key in self.keyboard:
            self.keyboard[key].set_status("normal")

    def make_guess(self, letter):
        if letter in self.guessed:
            return
        
        self.guessed.append(letter)
        correct = letter in self.word
        
        if correct:
            self.keyboard[letter].set_status("correct")
            self.sounds["correct"].play()
        else:
            self.hangman_status += 1
            self.keyboard[letter].set_status("incorrect")
            self.sounds["wrong"].play()
        
        # Check win/lose conditions
        display_word = ""
        for char in self.word:
            if char in self.guessed:
                display_word += char
            else:
                display_word += "_"
        
        won = "_" not in display_word
        lost = self.hangman_status >= 7
        
        if won or lost:
            self.game_state = GAME_OVER
            self.end_time = time.time()  # Store the end time when game is over
            game_time = self.end_time - self.start_time
            
            if won:
                self.score += 1
                self.sounds["win"].play()
                if self.score > self.high_score:
                    self.high_score = self.score
                
                if game_time < self.best_time or self.best_time == 0:
                    self.best_time = game_time
            else:
                self.score = 0
                self.sounds["lose"].play()

    def draw_hangman(self):
        # Draw the gallows
        pygame.draw.line(self.screen, BLACK, (100, 350), (180, 350), 3)  # Base
        pygame.draw.line(self.screen, BLACK, (140, 350), (140, 150), 3)  # Vertical post
        pygame.draw.line(self.screen, BLACK, (140, 150), (230, 150), 3)  # Horizontal beam
        
        # Draw hangman parts based on status
        if self.hangman_status >= 1:
            pygame.draw.line(self.screen, BLACK, (230, 150), (230, 170), 2)  # Rope
        
        if self.hangman_status >= 2:
            pygame.draw.circle(self.screen, BLACK, (230, 190), 20, 2)  # Head
        
        if self.hangman_status >= 3:
            pygame.draw.line(self.screen, BLACK, (230, 210), (230, 270), 2)  # Body
        
        if self.hangman_status >= 4:
            pygame.draw.line(self.screen, BLACK, (230, 230), (200, 220), 2)  # Left arm
        
        if self.hangman_status >= 5:
            pygame.draw.line(self.screen, BLACK, (230, 230), (260, 220), 2)  # Right arm
        
        if self.hangman_status >= 6:
            pygame.draw.line(self.screen, BLACK, (230, 270), (210, 310), 2)  # Left leg
        
        if self.hangman_status >= 7:
            pygame.draw.line(self.screen, BLACK, (230, 270), (250, 310), 2)  # Right leg
            # Draw face (X eyes and sad mouth)
            pygame.draw.line(self.screen, BLACK, (220, 185), (225, 190), 2)
            pygame.draw.line(self.screen, BLACK, (225, 185), (220, 190), 2)
            pygame.draw.line(self.screen, BLACK, (235, 185), (240, 190), 2)
            pygame.draw.line(self.screen, BLACK, (240, 185), (235, 190), 2)
            # Draw sad mouth (arc)
            pygame.draw.arc(self.screen, BLACK, (220, 195, 20, 10), 3.14, 2*3.14, 2)

    def draw_word_display(self):
        display_word = ""
        for char in self.word:
            if char in self.guessed:
                display_word += char + " "
            else:
                display_word += "_ "
        
        word_surface = get_font(40).render(display_word.strip(), True, DARK_COLOR)
        word_rect = word_surface.get_rect(center=(SCREEN_WIDTH // 2, 380))
        self.screen.blit(word_surface, word_rect)

    def draw_menu_screen(self):
        # Draw title
        title_surface = get_font(56).render("HANGMAN", True, PRIMARY_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 70))
        self.screen.blit(title_surface, title_rect)
        
        # Draw instructions
        subtitle = get_font(30).render("Select a Category", True, DARK_COLOR)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw category buttons
        for category, button in self.category_buttons:
            button.draw(self.screen)

    def draw_game_screen(self):
        # Draw title
        title_surface = get_font(40).render("HANGMAN", True, PRIMARY_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_surface, title_rect)
        
        # Draw game info
        info_bg = pygame.Rect(50, 90, SCREEN_WIDTH - 100, 50)
        pygame.draw.rect(self.screen, LIGHT_COLOR, info_bg, border_radius=10)
        
        # Score and high score
        score_text = f"Score: {self.score}"
        high_score_text = f"High Score: {self.high_score}"
        score_surface = get_font(18).render(score_text, True, DARK_COLOR)
        high_score_surface = get_font(18).render(high_score_text, True, DARK_COLOR)
        self.screen.blit(score_surface, (70, 100))
        self.screen.blit(high_score_surface, (70, 120))
        
        # Category
        category_text = f"Category: {self.current_category}"
        category_surface = get_font(18).render(category_text, True, DARK_COLOR)
        category_rect = category_surface.get_rect(center=(SCREEN_WIDTH // 2, 115))
        self.screen.blit(category_surface, category_rect)
        
        # Timer
        game_time = round(time.time() - self.start_time, 1) if self.game_state == PLAYING else 0
        best_time_text = f"Best: {round(self.best_time, 1)}s" if self.best_time > 0 else "Best: 0s"
        time_text = f"Time: {game_time}s"
        time_surface = get_font(18).render(time_text, True, DARK_COLOR)
        best_time_surface = get_font(18).render(best_time_text, True, DARK_COLOR)
        self.screen.blit(time_surface, (SCREEN_WIDTH - 180, 100))
        self.screen.blit(best_time_surface, (SCREEN_WIDTH - 180, 120))
        
        # Draw hangman
        self.draw_hangman()
        
        # Draw word display
        self.draw_word_display()
        
        # Draw keyboard
        for key in self.keyboard:
            self.keyboard[key].draw(self.screen)

    def draw_game_over_screen(self):
        # Draw title
        title_surface = get_font(40).render("HANGMAN", True, PRIMARY_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_surface, title_rect)
        
        # Check if won or lost
        won = self.hangman_status < 7
        
        # Draw result message
        result_text = "You Won!" if won else "Game Over"
        result_color = SUCCESS_COLOR if won else ERROR_COLOR
        result_surface = get_font(40).render(result_text, True, result_color)
        result_rect = result_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(result_surface, result_rect)
        
        # Draw word reveal
        word_reveal_text = f"The word was: {self.word}"
        word_surface = get_font(24).render(word_reveal_text, True, DARK_COLOR)
        word_rect = word_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(word_surface, word_rect)
        
        # Draw stats - Use the stored end_time instead of current time
        game_time = round(self.end_time - self.start_time, 1)
        best_time = round(self.best_time, 1) if self.best_time > 0 else 0
        
        stats_text1 = f"Score: {self.score} | High Score: {self.high_score}"
        stats_text2 = f"Time: {game_time}s | Best Time: {best_time}s"
        
        stats_surface1 = get_font(20).render(stats_text1, True, DARK_COLOR)
        stats_surface2 = get_font(20).render(stats_text2, True, DARK_COLOR)
        
        stats_rect1 = stats_surface1.get_rect(center=(SCREEN_WIDTH // 2, 250))
        stats_rect2 = stats_surface2.get_rect(center=(SCREEN_WIDTH // 2, 280))
        
        self.screen.blit(stats_surface1, stats_rect1)
        self.screen.blit(stats_surface2, stats_rect2)
        
        # Draw buttons
        self.play_again_btn.draw(self.screen)
        self.menu_btn.draw(self.screen)

    def run(self):
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Menu screen events
                if self.game_state == MENU:
                    for category, button in self.category_buttons:
                        button.check_hover(mouse_pos)
                        if button.is_clicked(event):
                            self.select_category(category)
                
                # Game screen events
                elif self.game_state == PLAYING:
                    for key in self.keyboard:
                        self.keyboard[key].check_hover(mouse_pos)
                        if self.keyboard[key].is_clicked(event):
                            self.make_guess(key)
                
                # Game over screen events
                elif self.game_state == GAME_OVER:
                    self.play_again_btn.check_hover(mouse_pos)
                    self.menu_btn.check_hover(mouse_pos)
                    
                    if self.play_again_btn.is_clicked(event):
                        self.reset_game()
                        self.select_category(self.current_category)
                    
                    if self.menu_btn.is_clicked(event):
                        self.game_state = MENU
                        self.reset_game()
            
            # Update button hover states
            if self.game_state == MENU:
                for _, button in self.category_buttons:
                    button.check_hover(mouse_pos)
            elif self.game_state == GAME_OVER:
                self.play_again_btn.check_hover(mouse_pos)
                self.menu_btn.check_hover(mouse_pos)
            
            # Draw the appropriate screen
            self.screen.fill(WHITE)
            
            if self.game_state == MENU:
                self.draw_menu_screen()
            elif self.game_state == PLAYING:
                self.draw_game_screen()
            elif self.game_state == GAME_OVER:
                self.draw_game_over_screen()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = HangmanGame()
    game.run() 