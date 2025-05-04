import speech_recognition as sr
import os
from mtranslate import translate
from translate import Translator
from colorama import Fore, Style, init
import threading

init(autoreset=True)


def Print_loop():
    while True:
        print(Fore.LIGHTGREEN_EX + "I am Lasting ", end="", flush=True)
        print(Style.RESET_ALL, end="", flush=True)


def Translate_H_E(txt):
    english = translate(txt, "en-in")
    return english

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 35000  #The ideal value for energy_threshold depends on the environment's noise level
    recognizer.dynamic_energy_adjustment_damping = 0.01
    recognizer.dynamic_energy_ratio = 1.0
    recognizer.pause_threshold = 0.3
    recognizer.operation_timeout = None
    recognizer.pause_threshold = 0.5
    recognizer.non_speaking_duration = 0.3

    while True:
        try:
            with sr.Microphone() as source:
                print(Fore.LIGHTGREEN_EX + "Adjusting for ambient noise...", flush=True)
                recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for 1 second
                print(Fore.LIGHTGREEN_EX + "Listening...", flush=True)

                audio = recognizer.listen(source, timeout=None)
                print("\r" + Fore.LIGHTYELLOW_EX + "Got it ", end="", flush=True)
                recognizer_text = recognizer.recognize_google(audio).lower()

                if recognizer_text:
                    translate_text = Translate_H_E(recognizer_text)
                    print("\r" + Fore.BLUE + "Mr Rajin: " + translate_text)
                    return translate_text
                else:
                    print(Fore.RED + "No text recognized.")
                    return "None"
        except sr.UnknownValueError:
            print(Fore.RED + "Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(Fore.RED + f"Could not request results; {e}")
        finally:
            print("\r", end="", flush=True)

        os.system("cls" if os.name =="nt" else "clear")
        # Start the listening thread
        listen_thread = threading.Thread(target=listen)
        print_thread = threading.Thread(target=Print_loop)

        listen_thread.start()
        print_thread.start()

        listen_thread.join()
        print_thread.join()


import speech_recognition as sr

def hearing():
    """Capture audio input and return recognized text."""
    recognizer = sr.Recognizer()
    # Adjust recognizer settings
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 3500  # Adjust based on the noise level in your environment
    recognizer.dynamic_energy_adjustment_damping = 0.01
    recognizer.dynamic_energy_ratio = 1.0
    recognizer.pause_threshold = 0.5
    recognizer.non_speaking_duration = 0.3

    with sr.Microphone() as source:  # Properly instantiate the Microphone object
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise

        while True:
            try:
                print("Listening for speech...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                recognized_txt = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {recognized_txt}")
                return recognized_txt
            except sr.UnknownValueError:
                print("Sorry, I did not understand the audio.")
                return ""
            except sr.WaitTimeoutError:
                print("Timeout: No speech detected.")
                return ""
            except sr.RequestError as e:
                print(f"Error with the recognition service: {e}")
                return ""
            finally:
                print("Waiting for the next input...\n")

