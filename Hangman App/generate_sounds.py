import numpy as np
import wave
import os
import struct

def generate_sine_wave(freq, duration, volume=0.5, sample_rate=44100):
    """Generate a sine wave at the given frequency, duration and volume."""
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    wave_data = np.sin(2 * np.pi * freq * t) * volume
    return wave_data

def generate_sound(filename, frequencies, duration, volume=0.5, sample_rate=44100):
    """Generate a sound file with the given frequencies and save it as WAV."""
    audio = np.zeros(int(duration * sample_rate))
    
    for freq in frequencies:
        audio += generate_sine_wave(freq, duration, volume / len(frequencies), sample_rate)
    
    # Normalize to 16-bit range and convert to int16
    audio = np.int16(audio / np.max(np.abs(audio)) * 32767 * 0.9)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Save as WAV file
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 2 bytes = 16 bits
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    
    print(f"Generated {filename}")

def main():
    print("Generating sound effects for Hangman pygame app...")
    
    # Create sounds directory if it doesn't exist
    os.makedirs("sounds", exist_ok=True)
    
    # Create correct.wav - a pleasant rising tone
    generate_sound("sounds/correct.wav", [440, 523, 659], 0.3, 0.7)
    
    # Create wrong.wav - a low error sound
    generate_sound("sounds/wrong.wav", [220, 196], 0.4, 0.7)
    
    # Create win.wav - a victory fanfare
    generate_sound("sounds/win.wav", [440, 554, 659, 880], 1.0, 0.8)
    
    # Create lose.wav - a sad descending tone
    generate_sound("sounds/lose.wav", [440, 392, 349, 293], 1.0, 0.7)
    
    print("All sound files generated successfully!")

if __name__ == "__main__":
    main() 