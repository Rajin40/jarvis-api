import sys
sys.path.append("D:/python/jervis")
from threading import Thread
import schedule
from backend.auto_tasks import run_schedule
import asyncio
import logging
import json
import os
from concurrent.futures import ThreadPoolExecutor
from rich import print
try:
    from backend.decisson_making_brain_model import FirstLayerDMM
    from backend.RealtimeSearchEngine import RealtimeSearchEngine
    from Chrome_Intregretion.function_intregation import Function_cmd
    from backend.british_brian_Voice import speak
    from backend.chatbot import ChatBot
    from backend.Voice import listen
except ImportError as e:
    print(f"Import error: {e}")
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLabel, QFrame, QPushButton, QStackedWidget, QSizePolicy, QLineEdit
)
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
CHAT_LOG_PATH = r"Data\ChatLog.json"
USERNAME = "Rajin"
ASSISTANT_NAME = "Jarvis"
current_dir = os.getcwd()
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

# Initialize files
os.makedirs(TempDirPath, exist_ok=True)
if not os.path.exists(rf'{TempDirPath}\Mic data'):
    with open(rf'{TempDirPath}\Mic data', "w", encoding='utf-8') as file:
        file.write("False")
if not os.path.exists(rf'{TempDirPath}\Status.data'):
    with open(rf'{TempDirPath}\Status.data', "w", encoding='utf-8') as file:
        file.write("")

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(rf'{TempDirPath}\Mic data', "w", encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    try:
        with open(rf'{TempDirPath}\Mic data', "r", encoding='utf-8') as file:
            Status = file.read()
        return Status
    except FileNotFoundError:
        return "False"

def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}\Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    try:
        with open(rf'{TempDirPath}\Status.data', "r", encoding='utf-8') as file:
            Status = file.read()
        return Status
    except FileNotFoundError:
        return ""

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def GraphicsDirectoryPath(Filename):
    return rf'{GraphicsDirPath}\{Filename}'

def TempDirectoryPath(Filename):
    return rf'{TempDirPath}\{Filename}'

def load_chat_history():
    try:
        with open(CHAT_LOG_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_chat_history(history):
    os.makedirs(os.path.dirname(CHAT_LOG_PATH), exist_ok=True)
    with open(CHAT_LOG_PATH, "w") as f:
        json.dump(history, f, indent=4)

def check_existing_response(query, chat_history):
    for i in range(len(chat_history) - 1, -1, -1):
        if chat_history[i].get("role") == "user" and chat_history[i].get("content", "").lower() == query.lower():
            if i + 1 < len(chat_history) and chat_history[i + 1].get("role") == "assistant":
                return chat_history[i + 1].get("content")
    return None

def run_async_query(query, chat_history):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(process_query(query, chat_history))
        return result
    finally:
        loop.close()

async def process_query(query, chat_history):
    logger.debug(f"Processing query: {query}")
    query_lower = query.lower()
    existing_response = check_existing_response(query, chat_history)
    if existing_response:
        logger.debug(f"Found existing response: {existing_response}")
        print(f"[{ASSISTANT_NAME}] (from memory): {existing_response}")
        speak(existing_response)
        return existing_response

    COMMAND_PHRASES = {
        "action_commands": [
            "open", "close", "play", "content", "google ", "search",
            "check internet speed", "check speed test", "speed test",
            "check temperature", "temperature", "temprature", "temprature outside",
            "find my ip", "ip address", "what is my ip", "check my ip", "give me my ip",
            "tell me my ip", "what is the time", "time", "what time is", "wagt kya hai",
            "samay kya hai", "kitne baje hain", "kitna samay hua", "tell the time",
            "what time is now", "tell me the time", "youtube search", "system", "check",
            "find", "visit", "launch", "search", "mute", "volume", "enter", "select",
            "copy", "paste", "undo", "scroll", "reload", "go back", "go forward", "stop",
            "maximize", "restore", "switch", "previous", "bookmark", "history", "downloads",
            "inspect", "clear", "fullscreen", "dark mode", "extensions", "settings",
            "save", "print", "new tab", "reopen", "show desktop", "virtual desktop",
            "notification", "action center", "lock screen", "log off", "shutdown", "restart",
            "sleep", "file explorer", "control panel", "navigate", "zoom", "search for",
            "start the work", "import gamil", "send mail", "send gmail", "send email",
            "send the mail", "send the email", "extract emails",
            "jervis you should do the linkedin post", "store the article", "store this article",
            "save the article", "save this article", "kholo", "show me", "minimise", "minimize",
            "type", "press enter", "select all", "copy this", "paste here", "undo karo",
            "back karo", "copy last paragraph", "increase volume", "volume badhao",
            "increase sound", "decrease volume", "volume kam karo", "decrease sound",
            "full volume", "full volume kr do", "mute this", "mute tab", "unmute",
            "unmute tab", "open browser settings", "browser settings", "save page as",
            "save as", "print page", "print", "clear browsing data", "clear history",
            "open bookmarks", "view bookmarks", "reload page", "refresh it", "go back",
            "back", "go forward", "forward", "stop loading", "stop", "scroll up",
            "scroll page up", "scroll down", "scroll page down", "scroll to top",
            "scroll to bottom", "open new tab", "new tab", "reopen closed tab",
            "restore closed tab", "navigate forward", "forward jao", "zoom in on the current page",
            "current page me zoom", "zoom out on the current page", "zoom out",
            "start clap with music system", "start smart music system",
            "post data science blog in website", "post data science blog",
            "post data scientist blog", "post data analysis blog in website",
            "post data analysis blog", "post data analyst blog",
            "post web development blog in website", "post web development blog",
            "post website development blog", "post digital marketing blog in website",
            "post digital marketing blog", "post graphic design blog in website",
            "post graphic design blog", "post statistical analysis blog in website",
            "post statistical analysis blog", "post statistical blog",
            "post market research blog in website", "post market research blog",
            "post market analysis blog in website", "post market analysis blog",
            "post market analyst blog", "store article for website", "save blog for website",
            "store blog for website", "write", "generate",
            "its time to post in website about data analysis",
            "its time to post in website about data science",
            "its time to post in website about web development",
            "its time to post in website about graphic design",
            "its time to post in website about market analysis",
            "its time to post in website about market research",
            "its time to post in website about digital marketing",
            "its time to post in website about statistical analysis",
            "generate code for", "create a script for", "make a python script for",
            "build a program for", "develop code for", "write code for",
            "generate plugin for", "create plugin for", "make plugin for",
            "code generation for", "create a python script"
        ],
        "search_phrases": [
            "who is", "what is", "do you know", "can you find", "i need",
            "i want", "how to", "what was", "who was", "real time data",
            "give me real time data", "give me real time information",
            "where is", "define", "teach me", "research"
        ],
        "exit_commands": ["exit", "quit", "bye"]
    }
    response = "I'm not sure how to respond to that."
    
    try:
        decisions = FirstLayerDMM(query)
        logger.debug(f"DMM decisions: {decisions}")
        if decisions:
            responses = []
            for decision in decisions:
                if any(phrase in query_lower for phrase in COMMAND_PHRASES["action_commands"]):
                    Function_cmd(decision)
                    responses.append(f"I've executed the command: {decision}")
                elif decision.startswith(("google", "youtube")):
                    Function_cmd(decision)
                    responses.append(f"I've performed the search: {decision}")
                elif decision.startswith("realtime") or any(phrase in query_lower for phrase in COMMAND_PHRASES["search_phrases"]):
                    realtime_query = decision[9:] if decision.startswith("realtime") else query
                    search_result = RealtimeSearchEngine(realtime_query)
                    responses.append(search_result if search_result else "No search results found.")
                elif decision == "exit":
                    return "exit"
                else:
                    general_query = decision.split(" ", 1)[1] if " " in decision else query
                    chat_response = ChatBot(general_query)
                    responses.append(chat_response if chat_response else "No response from ChatBot.")
            response = ". ".join(responses) if responses else response
        else:
            if any(phrase in query_lower for phrase in COMMAND_PHRASES["action_commands"]):
                Function_cmd(query)
                response = f"I've executed the command: {query}"
            elif any(phrase in query_lower for phrase in COMMAND_PHRASES["search_phrases"]):
                search_result = RealtimeSearchEngine(query)
                response = search_result if search_result else "No search results found."
            elif query_lower in COMMAND_PHRASES["exit_commands"]:
                return "exit"
            else:
                chat_response = ChatBot(query)
                response = chat_response if chat_response else "No response from ChatBot."
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        logger.error(error_msg)
        print(f"\n[{ASSISTANT_NAME}]: {error_msg}")
        speak(error_msg)
        return error_msg

    logger.debug(f"Response: {response}")
    print(f"[{ASSISTANT_NAME}]: {response}")
    speak(response)
    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": response})
    save_chat_history(chat_history)
    return response

class ChatSection(QWidget):
    def __init__(self, executor):
        super(ChatSection, self).__init__()
        self.executor = executor
        self.chat_history = load_chat_history()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 20)
        layout.setSpacing(10)
        
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message here...")
        self.input_box.setStyleSheet("background-color: white; color: black; font-size: 14px; padding: 5px; border-radius: 5px;")
        self.input_box.returnPressed.connect(self.sendMessage)
        input_layout.addWidget(self.input_box)
        
        send_button = QPushButton("Send")
        send_button.setStyleSheet("background-color: white; color: black; font-size: 14px; padding: 5px 10px; border-radius: 5px;")
        send_button.clicked.connect(self.sendMessage)
        input_layout.addWidget(send_button)
        
        layout.addLayout(input_layout)
        
        self.setStyleSheet("background-color:black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border:none;")
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        max_gif_size_W = 480
        max_gif_size_H = 340
        movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)
        
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-right: 195px; border: none; margin-top: -30px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(100)
        
        self.chat_text_edit.viewport().installEventFilter(self)
        
        self.setStyleSheet(self.styleSheet() + """
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: white;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                background: black;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                height: 10px;
            }
            QScrollBar::sub-line:vertical {
                background: black;
                subcontrol-position: top;
                subcontrol-origin: margin;
                height: 10px;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: none;
                background: none;
                color: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

    def sendMessage(self):
        query = self.input_box.text().strip()
        if query:
            modified_query = QueryModifier(query)
            self.addMessage(f"{USERNAME}: {modified_query}", color='blue')
            self.input_box.clear()
            QApplication.processEvents()
            logger.debug(f"Submitting query: {modified_query}")
            future = self.executor.submit(run_async_query, modified_query, self.chat_history)
            future.add_done_callback(self.handleResponse)

    def handleResponse(self, future):
        try:
            response = future.result()
            logger.debug(f"Handle response: {response}")
            if response and response != "exit":
                self.addMessage(f"{ASSISTANT_NAME}: {response}", color='white')
            elif response == "exit":
                QApplication.quit()
        except Exception as e:
            error_msg = f"Error processing response: {str(e)}"
            logger.error(error_msg)
            self.addMessage(f"{ASSISTANT_NAME}: {error_msg}", color='red')
        QApplication.processEvents()

    def SpeechRecogText(self):
        status = GetMicrophoneStatus()
        if status == "True":
            try:
                SetAssistantStatus("Listening...")
                self.label.setText("Listening...")
                QApplication.processEvents()
                user_input = listen()
                if user_input:
                    logger.debug(f"Voice input: {user_input}")
                    print(f"[{USERNAME}]: {user_input}")
                    modified_query = QueryModifier(user_input)
                    self.addMessage(f"{USERNAME}: {modified_query}", color='blue')
                    future = self.executor.submit(run_async_query, modified_query, self.chat_history)
                    future.add_done_callback(self.handleResponse)
                else:
                    SetAssistantStatus("")
                    self.label.setText("")
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                logger.error(error_msg)
                print(f"\n[{ASSISTANT_NAME}]: {error_msg}")
                speak(error_msg)
                self.addMessage(f"{ASSISTANT_NAME}: {error_msg}", color='red')
                self.label.setText("Error occurred")
        else:
            SetAssistantStatus("")
            self.label.setText("")
        QApplication.processEvents()

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)
        self.chat_text_edit.ensureCursorVisible()
        QApplication.processEvents()

class InitialScreen(QWidget):
    def __init__(self, executor):
        super().__init__()
        self.executor = executor
        self.chat_history = load_chat_history()
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.setContentsMargins(0, 200, 0, 0)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 80)
        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        movie.setCacheMode(QMovie.CacheAll)
        gif_width = 1100
        gif_height = int(gif_width / 12 * 9)
        movie.setScaledSize(QSize(gif_width, gif_height))
        movie.loopCount = -1
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        self.icon_label = QLabel()
        pixmap = QPixmap(GraphicsDirectoryPath('Mic_on.png'))
        new_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-bottom:0;")
        self.label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(gif_label)
        content_layout.addWidget(self.label)
        content_layout.addWidget(self.icon_label)
        outer_layout.addWidget(content_widget)
        self.setLayout(outer_layout)
        self.setFixedSize(screen_width, screen_height)
        self.setStyleSheet("background-color: black;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(100)

    def SpeechRecogText(self):
        status = GetMicrophoneStatus()
        if status == "True":
            try:
                SetAssistantStatus("Listening...")
                self.label.setText("Listening...")
                QApplication.processEvents()
                user_input = listen()
                if user_input:
                    logger.debug(f"Voice input: {user_input}")
                    print(f"[{USERNAME}]: {user_input}")
                    modified_query = QueryModifier(user_input)
                    self.label.setText(f"{USERNAME}: {modified_query}")
                    future = self.executor.submit(run_async_query, modified_query, self.chat_history)
                    future.add_done_callback(self.handleVoiceResponse)
                else:
                    SetAssistantStatus("")
                    self.label.setText("")
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                logger.error(error_msg)
                print(f"\n[{ASSISTANT_NAME}]: {error_msg}")
                speak(error_msg)
                self.label.setText("Error occurred")
        else:
            SetAssistantStatus("")
            self.label.setText("")
        QApplication.processEvents()

    def handleVoiceResponse(self, future):
        try:
            response = future.result()
            logger.debug(f"Voice response: {response}")
            if response and response != "exit":
                self.label.setText(f"{ASSISTANT_NAME}: {response}")
            elif response == "exit":
                QApplication.quit()
        except Exception as e:
            error_msg = f"Error processing voice response: {str(e)}"
            logger.error(error_msg)
            self.label.setText(f"{ASSISTANT_NAME}: {error_msg}")
        QApplication.processEvents()

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
            MicButtonClosed()
        self.toggled = not self.toggled

class MessageScreen(QWidget):
    def __init__(self, executor):
        super().__init__()
        self.executor = executor
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        layout = QVBoxLayout()
        labelsthe = QLabel("")
        layout.addWidget(labelsthe)
        chat_section = ChatSection(executor)
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.current_screen = None
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        home_button = QPushButton()
        home_icon = QIcon(GraphicsDirectoryPath("Home.png"))
        home_button.setIcon(home_icon)
        home_button.setText("  Home")
        home_button.setStyleSheet("height:40px; line-height: 40px; background-color:white; color: black")
        message_button = QPushButton()
        message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText("    Chat")
        message_button.setStyleSheet("height:40px; line-height:40px; background-color:white; color: black")
        minimize_button = QPushButton()
        minimize_icon = QIcon(GraphicsDirectoryPath('Minimize2.png'))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("background-color:white")
        minimize_button.clicked.connect(self.minimizeWindow)
        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicsDirectoryPath('Maximize.png'))
        self.restore_icon = QIcon(GraphicsDirectoryPath('Minimize.png'))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("background-color:white")
        self.maximize_button.clicked.connect(self.maximizeWindow)
        close_button = QPushButton()
        close_icon = QIcon(GraphicsDirectoryPath('Close.png'))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color:white")
        close_button.clicked.connect(self.closeWindow)
        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color: black;")
        title_label = QLabel(f"{str(ASSISTANT_NAME).capitalize()} AI    ")
        title_label.setStyleSheet("color: black; font-size: 18px; background-color:white")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)
        self.draggable = True
        self.offset = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable and event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset is not None and event.buttons() & Qt.LeftButton:
            self.parent().move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.initUI()
        Thread(target=run_schedule).start()

    def initUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen(self.executor)
        message_screen = MessageScreen(self.executor)
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet("background-color: black;")
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

    def closeEvent(self, event):
        self.executor.shutdown(wait=True)
        event.accept()

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()