import sys
sys.path.append("D:/python/jervis")
from open_everything.open_auto import *
from search_google import *
from scrol_auto import *
from tab_auto import *
from close_eveything.common_Intregrate import *

def google_cmd(text):
    if "open" in text:
        if "website" in text or "site" in text:
            text = text.replace("open","")
            text = text.replace("website","")
            text = text.replace("site","")
            text = text.strip()
            open_website(text)
        else:
            text = text.replace("open","")
            text = text.strip()
            if text == "":
                pass
            else:
                open(text)

    elif "scroll up" in text.lower():
        scroll_up()
    elif "scroll down" in text.lower():
        scroll_down()
    elif "scroll to top" in text.lower():
        scroll_to_top()
    elif "scroll to bottom" in text.lower():
        scroll_to_bottom()


    elif text.endswith("search in google") or text.startswith("search on google"):
        text = text. replace ("search in google","")
        text = text. replace("search on google","")
        search_google(text)

    elif "open new tab" in text:
        open_new_tab()
    elif "close tab" in text:
        close_tab()
    elif "reopen closed tab" in text:
        reopen_closed_tab()
    elif "next tab" in text:
        go_to_next_tab()
    elif "previous tab" in text:
        go_to_previous_tab()
    elif "go back" in text:
        go_back()
    elif "go forward" in text:
        go_forward()
    elif "refresh" in text:
        refresh_page()
    elif "hard refresh" in text:
        hard_refresh()
    elif "stop loading" in text:
        stop_loading()
    elif "open new window" in text:
        open_new_window()
    elif "open incognito window" in text:
        open_incognito_window()
    elif "minimize window" in text:
        minimize_window()
    elif "maximize window" in text:
        maximize_window()
    elif "focus address bar" in text:
        focus_address_bar()
    elif "open search" in text:
        open_search()
    elif "search highlighted text" in text:
        search_highlighted_text()
    elif "copy" in text:
        copy()
    elif "paste" in text:
        paste()
    elif "cut" in text:
        cut()
    elif "zoom in" in text:
        zoom_in()
    elif "zoom out" in text:
        zoom_out()
    elif "reset zoom" in text:
        reset_zoom()
    else:
        pass

