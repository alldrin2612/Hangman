import os
import subprocess
import sys

def setup():
    """Set up the Hangman game by installing requirements and generating assets."""
    print("Setting up Hangman Game...")
    
    # Install requirements
    print("\n1. Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Packages installed successfully!")
    except Exception as e:
        print(f"Error installing packages: {e}")
        print("Please install the packages manually using: pip install -r requirements.txt")
    
    # Download font
    print("\n2. Downloading font...")
    try:
        import download_font
        download_font.download_font()
    except Exception as e:
        print(f"Error downloading font: {e}")
        print("Please download Comic Neue font manually and place it in the 'fonts' directory.")
    
    # Generate sounds
    print("\n3. Generating sounds...")
    try:
        import generate_sounds
        generate_sounds.main()
    except Exception as e:
        print(f"Error generating sounds: {e}")
        print("Please run generate_sounds.py manually.")
    
    print("\nSetup complete! You can now run the game with: python hangman_game.py")

if __name__ == "__main__":
    # Change to script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    setup() 