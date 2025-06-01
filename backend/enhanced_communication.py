from backend.british_brian_Voice import speak
from googletrans import Translator
from textblob import TextBlob
import speech_recognition as sr

# Initialize translator for multi-language support
translator = Translator()

# Listen to the user and recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            speak("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            speak("Could not request results; check your network connection.")
            return None

# Detect language of the speech
def detect_language(text):
    detected = translator.detect(text)
    return detected.lang

# Translate text to a target language (e.g., English)
def translate_text(text, target_language='en'):
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Analyze sentiment using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity  # Value between -1 (negative) and 1 (positive)
    sentiment = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
    return sentiment, sentiment_score

# Handle the user's command
def handle_command(text):
    # Detect the language of the input text
    language = detect_language(text)
    print(f"Detected Language: {language}")

    # Translate to English if the input language is not English
    if language != 'en':
        translated_text = translate_text(text, target_language='en')
        speak(f"Translation: {translated_text}")
    else:
        translated_text = text

    # Perform emotion analysis
    sentiment, _ = analyze_sentiment(translated_text)

    # Provide responses based on sentiment
    if sentiment == "Negative":
        speak("You seem upset. How can I help?")
    elif sentiment == "Positive":
        speak("I'm glad you're in a good mood!")
    else:
        speak("I detected a neutral tone.")

    # Add further functionality here like AR/VR control, home automation, etc.
    # Example: send_action_to_unity("change color") - This can be added as per the context

# Main loop to listen, analyze, and respond
#if __name__ == "__main__":
   #speak("Hello! How can I assist you today?")
    #while True:
        #user_command = recognize_speech()
        #if user_command:
         #   handle_command(user_command)
