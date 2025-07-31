import pyttsx3
import time

# Initialize the TTS engine
engine = pyttsx3.init()

# Configure voice properties (optional)
voices = engine.getProperty('voices')
engine.setProperty('rate', 180)  # Speed of speech
if voices:  # Set the first available voice
    engine.setProperty('voice', voices[0].id)

def speak(text):
    try:
        print(text)
        engine.say(text)
        engine.runAndWait()
        
        # Calculate sleep duration based on sentence length
        sleep_duration = min(0.1 + len(text) // 20, 5)  # Minimum sleep is 0.1 seconds, maximum is 5 seconds
        time.sleep(sleep_duration)
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
speak("Hello, this is an offline text-to-speech example.")

# When done, you can optionally stop the engine
engine.stop()