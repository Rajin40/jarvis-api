import datetime
import sys
sys.path.append("D:/python/jervis")



def what_is_the_time():
    try:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        print(f"The time is {current_time}")

    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        print(error_message)

