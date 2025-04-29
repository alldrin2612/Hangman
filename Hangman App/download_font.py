import os
import urllib.request
import zipfile
import shutil

def download_font():
    """Download and extract the Comic Neue font."""
    print("Downloading Comic Neue font...")
    
    # Create fonts directory if it doesn't exist
    os.makedirs("fonts", exist_ok=True)
    
    # Download Comic Neue
    font_url = "https://fonts.google.com/download?family=Comic%20Neue"
    zip_path = "ComicNeue.zip"
    
    try:
        # Download the zip file
        urllib.request.urlretrieve(font_url, zip_path)
        
        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("fonts_temp")
        
        # Copy the TTF files to fonts directory
        for font_file in os.listdir("fonts_temp/static"):
            if font_file.endswith(".ttf") and "Bold" in font_file:
                shutil.copy(os.path.join("fonts_temp/static", font_file), 
                           os.path.join("fonts", "ComicNeue-Bold.ttf"))
                break
        
        # Clean up
        shutil.rmtree("fonts_temp")
        os.remove(zip_path)
        
        print("Comic Neue font downloaded successfully!")
    
    except Exception as e:
        print(f"Error downloading font: {e}")
        print("Please download Comic Neue font manually and place it in the 'fonts' directory.")

if __name__ == "__main__":
    download_font() 