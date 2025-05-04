import sys
sys.path.append("D:/python/jervis")
from backend.big_data import *
from backend.small_data import *
from backend.British_Brian_Voice import *
from LLM_file.llm1 import *
from load_file import *
from backend.Voice import listen
from DLG import *
from Emotional_model.Machine_Learning_Enhancements import *

def brain_cmd(text):
    if "jarvis" in text:
        text = text.replace("jarvis","")
        text = text.strip()
        if text in qa_dict:
            ans = qa_dict[text]
        elif "define" in text or "brief" in text or "research" in text or "teach me" in text:
           ans = deep_search(text)
        elif text.startswith(("who is","what is","do you know","can you find","i need","i want","how to","what was","who was","real time data","give me real time data","where is")):
            ans = search_brain(text)

        elif text in emotion:
            ans = analyze_sentiment(text)
            speak(ans)

        else:
            ans = llm1.llm1(text)

        return ans
    else:
        pass

# Example usage
result = brain_cmd("The service was excellent, I'm very satisfied!")
print(result)


while True:
    text = input("Enter Your Question: ")
    x= brain_cmd (text)
    speak(x)
