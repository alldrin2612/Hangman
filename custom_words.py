"""
Custom word lists for the Hangman game with difficulty categorization
"""

# Easy words (4-6 letters)
EASY_WORDS = [
    'BALL', 'TREE', 'FISH', 'DOOR', 'BOOK', 'LAMP', 'CHAIR', 'TABLE', 
    'WATER', 'BREAD', 'HOUSE', 'CLOCK', 'PLATE', 'APPLE', 'SHIRT',
    'SHOES', 'SMILE', 'WORLD', 'PHONE', 'PAPER', 'MUSIC', 'BEACH',
    'LIGHT', 'RIVER', 'CLOUD', 'GREEN'
]

# Medium words (7-9 letters)
MEDIUM_WORDS = [
    'COMPUTER', 'BIRTHDAY', 'ELEPHANT', 'BASEBALL', 'COMPLETE', 'MOUNTAIN',
    'DAUGHTER', 'QUESTION', 'AIRPLANE', 'INDUSTRY', 'CHILDREN', 'BUILDING',
    'KNOWLEDGE', 'EXERCISE', 'KEYBOARD', 'TRIANGLE', 'VACATION', 'FAVORITE',
    'SANDWICH', 'TOMORROW', 'CONFUSED', 'TOMORROW', 'PAINTING', 'WEATHER'
]

# Hard words (10+ letters)
HARD_WORDS = [
    'DEVELOPMENT', 'COMFORTABLE', 'RESPONSIBLE', 'CELEBRATION', 'COMMUNITY',
    'INTELLIGENCE', 'COMMUNICATION', 'REFRIGERATOR', 'UNDERSTANDING', 'ADVERTISEMENT',
    'IMAGINATION', 'PROFESSIONAL', 'RELATIONSHIP', 'OPPORTUNITY', 'CONVERSATION',
    'DETERMINATION', 'ENVIRONMENT', 'PHOTOGRAPHY', 'QUALIFICATION', 'EXTRAORDINARY',
    'UNPREDICTABLE', 'SOPHISTICATED', 'REVOLUTIONARY', 'ORGANIZATION'
]

# Topic-based words
ANIMALS = [
    'ELEPHANT', 'GIRAFFE', 'DOLPHIN', 'PENGUIN', 'KANGAROO', 'LEOPARD',
    'TURTLE', 'SQUIRREL', 'CROCODILE', 'BUTTERFLY', 'OCTOPUS', 'RABBIT',
    'TIGER', 'PANTHER', 'ZEBRA', 'MONKEY', 'PEACOCK', 'EAGLE', 'FOX'
]

COUNTRIES = [
    'AUSTRALIA', 'CANADA', 'GERMANY', 'BRAZIL', 'FRANCE', 'JAPAN', 'MEXICO',
    'RUSSIA', 'SWEDEN', 'THAILAND', 'EGYPT', 'PORTUGAL', 'ARGENTINA', 'KENYA',
    'SWITZERLAND', 'NIGERIA', 'DENMARK', 'INDONESIA', 'MALAYSIA', 'GREECE'
]

PROGRAMMING = [
    'PYTHON', 'JAVASCRIPT', 'FUNCTION', 'VARIABLE', 'ALGORITHM', 'PARAMETER',
    'STRING', 'INTEGER', 'BOOLEAN', 'OBJECT', 'ARRAY', 'DATABASE', 'FRAMEWORK',
    'INTERFACE', 'METHOD', 'INHERITANCE', 'DEBUGGING', 'COMPILER', 'RECURSION'
]

# Dictionary of all word categories
WORD_CATEGORIES = {
    'EASY': EASY_WORDS,
    'MEDIUM': MEDIUM_WORDS,
    'HARD': HARD_WORDS,
    'ANIMALS': ANIMALS,
    'COUNTRIES': COUNTRIES,
    'PROGRAMMING': PROGRAMMING
}

# Function to get words by difficulty or category
def get_words(category):
    """
    Get words from a specific category or difficulty level
    
    Args:
        category (str): The category or difficulty level to get words from
        
    Returns:
        list: A list of words from the specified category
    """
    category = category.upper()
    return WORD_CATEGORIES.get(category, MEDIUM_WORDS)  # Default to medium words

# Function to get all available categories
def get_categories():
    """
    Get all available word categories
    
    Returns:
        list: A list of all available word categories
    """
    return list(WORD_CATEGORIES.keys())

# The following functions are kept for compatibility but not used in the web version
def save_custom_words(words, filename="custom_words.txt"):
    """
    Save a list of custom words to a file
    
    Args:
        words (list): List of words to save
        filename (str, optional): Filename to save to. Defaults to "custom_words.txt".
    """
    try:
        with open(filename, "w") as f:
            for word in words:
                f.write(word.upper() + "\n")
        return True
    except Exception as e:
        print(f"Error saving custom words: {e}")
        return False

def load_custom_words(filename="custom_words.txt"):
    """
    Load custom words from a file
    
    Args:
        filename (str, optional): Filename to load from. Defaults to "custom_words.txt".
        
    Returns:
        list: A list of words loaded from the file
    """
    try:
        words = []
        with open(filename, "r") as f:
            for line in f:
                word = line.strip().upper()
                if word:
                    words.append(word)
        return words
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading custom words: {e}")
        return []

# Add custom words to the word categories
WORD_CATEGORIES['CUSTOM'] = load_custom_words() 