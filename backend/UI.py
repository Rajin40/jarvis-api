import sys
import os
import json
import asyncio
import time
import psutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QSplitter, QFrame,
    QListWidget, QComboBox, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QTextCursor, QIcon, QPalette, QColor, QPixmap

# Set environment variables before other imports
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings

# Import your custom modules
sys.path.append("D:/python/jervis")
from backend.decisson_making_brain_model import FirstLayerDMM
from backend.RealtimeSearchEngine import RealtimeSearchEngine
from backend.Automation import Automation
from backend.British_Brian_Voice import speak
from backend.Chatbot import ChatBot
from backend.Voice import listen

class AnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.OutQuad)
        
    def enterEvent(self, event):
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(-2, -2, 4, 4))
        self._animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(2, 2, -4, -4))
        self._animation.start()
        super().leaveEvent(event)

class SystemMonitorThread(QThread):
    update_signal = pyqtSignal(dict)
    
    def run(self):
        while True:
            try:
                stats = {
                    'cpu': int(psutil.cpu_percent()),
                    'memory': int(psutil.virtual_memory().percent)
                }
                self.update_signal.emit(stats)
                time.sleep(2)
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(5)

class VoiceWorker(QThread):
    voice_result = pyqtSignal(str)
    listening_changed = pyqtSignal(bool)
    
    def run(self):
        try:
            self.listening_changed.emit(True)
            text = listen()
            self.listening_changed.emit(False)
            self.voice_result.emit(text)
        except Exception as e:
            self.listening_changed.emit(False)
            self.voice_result.emit("")

class WorkerThread(QThread):
    finished_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    typing_signal = pyqtSignal(str)

    def __init__(self, query, chat_history):
        super().__init__()
        self.query = query
        self.chat_history = chat_history

    def run(self):
        async def run_async():
            return await self.process_query()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_async())
        loop.close()
        self.finished_signal.emit(result)

    async def process_query(self):
        """Process user query through the decision making model and route accordingly"""
        self.status_signal.emit("Checking memory...")
        existing_response = self.check_existing_response()
        if existing_response:
            return existing_response
        
        self.status_signal.emit("Analyzing query...")
        decision = FirstLayerDMM(self.query)
        self.status_signal.emit(f"Decision: {decision}")
        
        if not decision:
            decision = ["general (query)"]
        
        responses = []
        
        for task in decision:
            if task.startswith("general"):
                self.status_signal.emit("Generating response...")
                response = ChatBot(self.query)
                responses.append(response)
            elif task.startswith("realtime"):
                search_query = task.replace("realtime", "").strip("() ")
                self.status_signal.emit("Searching real-time information...")
                response = RealtimeSearchEngine(search_query or self.query)
                responses.append(response)
            elif task.startswith(("open", "close", "play", "content", "google search", "youtube search", "system")):
                self.status_signal.emit(f"Executing command: {task}")
                await Automation([task])
                responses.append(f"Executed: {task}")
            elif task == "exit":
                responses.append("Goodbye!")
                return "exit"
            else:
                self.status_signal.emit("Generating response...")
                response = ChatBot(self.query)
                responses.append(response)
        
        return " ".join(responses)

    def check_existing_response(self):
        """Check if the query has already been answered in chat history"""
        for i in range(len(self.chat_history)-1, -1, -1):
            if self.chat_history[i]["role"] == "user" and self.chat_history[i]["content"].lower() == self.query.lower():
                if i+1 < len(self.chat_history) and self.chat_history[i+1]["role"] == "assistant":
                    return self.chat_history[i+1]["content"]
        return None

class JARVISUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS Personal Assistant")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize attributes
        self.chat_history = []
        self.command_history = []
        self.settings = {"theme": "Dark"}
        
        # Load data
        self.load_settings()
        self.load_chat_history()
        
        # Setup UI
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.setup_animations()
        
        # Start system monitor
        self.system_monitor = SystemMonitorThread()
        self.system_monitor.update_signal.connect(self.update_system_stats)
        self.system_monitor.start()
        
        # Show welcome message
        self.add_message("JARVIS", "Hello! How can I assist you today?", is_user=False)

    def create_widgets(self):
        """Initialize all UI widgets"""
        # Output screen
        self.output_screen = QTextEdit()
        self.output_screen.setReadOnly(True)
        
        # Status screen
        self.status_screen = QTextEdit()
        self.status_screen.setReadOnly(True)
        self.status_screen.setMaximumHeight(120)
        
        # Command history
        self.command_history_widget = QListWidget()
        self.command_history_widget.setMaximumWidth(200)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message or command here...")
        
        # Buttons
        self.send_button = AnimatedButton("Send")
        self.mic_button = AnimatedButton()
        self.mic_button.setIcon(QIcon("mic_icon.png"))
        self.mic_button.setToolTip("Voice Input")
        
        # System stats
        self.cpu_bar = QProgressBar()
        self.memory_bar = QProgressBar()
        self.setup_progress_bars()
        
        # Theme selector
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Dark", "Light", "Blue", "Green", "Purple"])
        self.theme_selector.setCurrentText(self.settings.get("theme", "Dark"))
        
        # Typing indicator
        self.typing_label = QLabel()
        self.typing_label.setAlignment(Qt.AlignRight)
        self.typing_label.hide()

    def setup_progress_bars(self):
        """Configure progress bars appearance"""
        for bar in [self.cpu_bar, self.memory_bar]:
            bar.setRange(0, 100)
            bar.setTextVisible(False)
            bar.setValue(0)

    def create_layout(self):
        """Setup the main window layout"""
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Horizontal split for main content
        horizontal_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel (command history)
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Command History"))
        left_layout.addWidget(self.command_history_widget)
        
        # Right panel (main content)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)
        
        # Output area
        output_frame = QFrame()
        output_layout = QVBoxLayout(output_frame)
        output_layout.addWidget(QLabel("Conversation"))
        output_layout.addWidget(self.output_screen)
        
        # Status area
        status_frame = QFrame()
        status_layout = QVBoxLayout(status_frame)
        status_layout.addWidget(QLabel("System Status"))
        status_layout.addWidget(self.status_screen)
        
        # System stats area
        stats_frame = QFrame()
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.addWidget(QLabel("CPU:"))
        stats_layout.addWidget(self.cpu_bar)
        stats_layout.addWidget(QLabel("RAM:"))
        stats_layout.addWidget(self.memory_bar)
        
        # Combine right panel
        right_layout.addWidget(output_frame)
        right_layout.addWidget(status_frame)
        right_layout.addWidget(stats_frame)
        
        # Add to horizontal splitter
        horizontal_splitter.addWidget(left_panel)
        horizontal_splitter.addWidget(right_panel)
        horizontal_splitter.setSizes([200, 800])
        
        # Input area
        input_frame = QFrame()
        input_layout = QHBoxLayout(input_frame)
        input_layout.addWidget(self.input_field, 5)
        input_layout.addWidget(self.mic_button, 1)
        input_layout.addWidget(self.send_button, 1)
        
        # Bottom controls
        bottom_frame = QFrame()
        bottom_layout = QHBoxLayout(bottom_frame)
        bottom_layout.addWidget(self.typing_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(QLabel("Theme:"))
        bottom_layout.addWidget(self.theme_selector)
        
        # Combine all layouts
        main_layout.addWidget(horizontal_splitter)
        main_layout.addWidget(input_frame)
        main_layout.addWidget(bottom_frame)
        
        self.setCentralWidget(main_widget)
        self.apply_theme(self.theme_selector.currentText())

    def create_connections(self):
        """Connect signals to slots"""
        self.send_button.clicked.connect(self.process_input)
        self.input_field.returnPressed.connect(self.process_input)
        self.mic_button.clicked.connect(self.start_voice_input)
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        self.command_history_widget.itemClicked.connect(self.reuse_command)

    def setup_animations(self):
        """Setup UI animations"""
        self.typing_animation = QPropertyAnimation(self.typing_label, b"windowOpacity")
        self.typing_animation.setDuration(1000)
        self.typing_animation.setStartValue(0.5)
        self.typing_animation.setEndValue(1.0)
        self.typing_animation.setLoopCount(-1)
        self.typing_animation.setEasingCurve(QEasingCurve.InOutQuad)

    def load_settings(self):
        """Load application settings"""
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    self.settings = json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_settings(self):
        """Save application settings"""
        try:
            with open("settings.json", "w") as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_chat_history(self):
        """Load chat history from file"""
        try:
            chat_log_path = os.path.join("Data", "ChatLog.json")
            if os.path.exists(chat_log_path):
                with open(chat_log_path, "r") as f:
                    self.chat_history = json.load(f)
                    # Populate command history
                    for item in self.chat_history:
                        if item["role"] == "user":
                            text = item["content"][:50] + ("..." if len(item["content"]) > 50 else "")
                            self.command_history_widget.addItem(text)
        except Exception as e:
            print(f"Error loading chat history: {e}")

    def save_chat_history(self):
        """Save chat history to file"""
        try:
            os.makedirs("Data", exist_ok=True)
            with open(os.path.join("Data", "ChatLog.json"), "w") as f:
                json.dump(self.chat_history, f, indent=4)
        except Exception as e:
            print(f"Error saving chat history: {e}")

    def add_message(self, sender, message, is_user=True):
        """Add a message to the conversation"""
        cursor = self.output_screen.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        if is_user:
            cursor.insertHtml(f'<div style="color: #64B5F6; font-weight: bold; margin-bottom: 5px;">{sender}:</div>')
        else:
            cursor.insertHtml(f'<div style="color: #81C784; font-weight: bold; margin-bottom: 5px;">{sender}:</div>')
        
        cursor.insertText(f"{message}\n\n")
        self.output_screen.ensureCursorVisible()

    def update_status(self, message):
        """Update the status screen"""
        cursor = self.status_screen.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(f"> {message}\n")
        self.status_screen.ensureCursorVisible()

    def update_system_stats(self, stats):
        """Update system monitoring displays"""
        self.cpu_bar.setValue(stats['cpu'])
        self.memory_bar.setValue(stats['memory'])
        
        # Change color based on usage
        for bar, value in [(self.cpu_bar, stats['cpu']), (self.memory_bar, stats['memory'])]:
            if value > 80:
                color = "#F44336"
            elif value > 60:
                color = "#FFC107"
            else:
                color = "#4CAF50"
            
            bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 1px solid #3A3A50;
                    border-radius: 5px;
                    background-color: #252538;
                    height: 10px;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 5px;
                }}
            """)

    def process_input(self):
        """Process user input from text field"""
        try:
            query = self.input_field.text().strip()
            if not query:
                return
                
            self.input_field.clear()
            self.add_message("You", query)
            
            # Add to command history
            display_text = query[:50] + ("..." if len(query) > 50 else "")
            self.command_history_widget.addItem(display_text)
            
            # Add to chat history
            self.chat_history.append({"role": "user", "content": query})
            
            # Show typing indicator
            self.typing_label.setText("JARVIS is typing...")
            self.typing_label.show()
            self.typing_animation.start()
            
            # Start worker thread
            self.worker = WorkerThread(query, self.chat_history)
            self.worker.finished_signal.connect(self.handle_response)
            self.worker.status_signal.connect(self.update_status)
            self.worker.start()
            
        except Exception as e:
            print(f"Input processing error: {e}")
            self.add_message("System", f"Error: {str(e)}", is_user=False)

    def start_voice_input(self):
        """Start voice input recording"""
        self.update_status("Listening... Speak now")
        self.mic_button.setEnabled(False)
        
        # Visual feedback for listening state
        self.mic_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 15px;
            }
        """)
        
        # Run voice recognition
        self.voice_worker = VoiceWorker()
        self.voice_worker.voice_result.connect(self.handle_voice_result)
        self.voice_worker.listening_changed.connect(self.update_mic_state)
        self.voice_worker.start()

    def update_mic_state(self, listening):
        """Update microphone button state"""
        if listening:
            self.mic_button.setStyleSheet("""
                QPushButton {
                    background-color: #F44336;
                    color: white;
                    border: none;
                    border-radius: 15px;
                }
            """)
        else:
            self.mic_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 15px;
                }
            """)
            self.mic_button.setEnabled(True)

    def handle_voice_result(self, text):
        """Handle voice recognition result"""
        if text:
            self.input_field.setText(text)
            self.process_input()

    def handle_response(self, response):
        """Handle response from worker thread"""
        # Hide typing indicator
        self.typing_animation.stop()
        self.typing_label.hide()
        
        if response == "exit":
            self.close()
            return
            
        self.add_message("JARVIS", response, is_user=False)
        self.chat_history.append({"role": "assistant", "content": response})
        self.save_chat_history()
        speak(response)

    def reuse_command(self, item):
        """Reuse a command from history"""
        text = item.text()
        for msg in reversed(self.chat_history):
            if msg["role"] == "user" and msg["content"].startswith(text.replace("...", "")):
                self.input_field.setText(msg["content"])
                self.input_field.setFocus()
                break

    def change_theme(self, theme_name):
        """Change application theme"""
        self.settings["theme"] = theme_name
        self.save_settings()
        self.apply_theme(theme_name)

    def apply_theme(self, theme_name):
        """Apply selected theme to UI"""
        palette = QPalette()
        
        if theme_name == "Dark":
            base_color = QColor(30, 30, 46)
            text_color = QColor(224, 224, 224)
            highlight_color = QColor(65, 105, 225)
        elif theme_name == "Light":
            base_color = QColor(240, 240, 240)
            text_color = QColor(0, 0, 0)
            highlight_color = QColor(100, 149, 237)
        elif theme_name == "Blue":
            base_color = QColor(23, 42, 58)
            text_color = QColor(200, 230, 255)
            highlight_color = QColor(0, 168, 255)
        elif theme_name == "Green":
            base_color = QColor(30, 46, 30)
            text_color = QColor(200, 255, 200)
            highlight_color = QColor(76, 175, 80)
        elif theme_name == "Purple":
            base_color = QColor(46, 30, 46)
            text_color = QColor(230, 200, 255)
            highlight_color = QColor(156, 39, 176)
        
        # Set palette colors
        palette.setColor(QPalette.Window, base_color)
        palette.setColor(QPalette.WindowText, text_color)
        palette.setColor(QPalette.Base, base_color.darker(120))
        palette.setColor(QPalette.AlternateBase, base_color)
        palette.setColor(QPalette.ToolTipBase, text_color)
        palette.setColor(QPalette.ToolTipText, text_color)
        palette.setColor(QPalette.Text, text_color)
        palette.setColor(QPalette.Button, base_color)
        palette.setColor(QPalette.ButtonText, text_color)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, highlight_color)
        palette.setColor(QPalette.Highlight, highlight_color)
        palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(palette)
        
        # Update widget styles
        self.output_screen.setStyleSheet(f"""
            font-size: 14px;
            background-color: {base_color.darker(120).name()};
            color: {text_color.name()};
            border-radius: 10px;
            padding: 10px;
            border: 1px solid {highlight_color.name()};
        """)
        
        self.status_screen.setStyleSheet(f"""
            font-size: 12px;
            color: {text_color.name()};
            background-color: {base_color.darker(150).name()};
            border-radius: 8px;
            padding: 8px;
            border: 1px solid {highlight_color.name()};
        """)
        
        self.command_history_widget.setStyleSheet(f"""
            font-size: 12px;
            background-color: {base_color.darker(150).name()};
            color: {text_color.name()};
            border-radius: 8px;
            padding: 5px;
            border: 1px solid {highlight_color.name()};
        """)
        
        self.input_field.setStyleSheet(f"""
            font-size: 14px;
            padding: 10px;
            border-radius: 15px;
            background-color: {base_color.darker(150).name()};
            color: {text_color.name()};
            border: 1px solid {highlight_color.name()};
        """)

def show_splash():
    """Show splash screen if image exists"""
    splash = None
    try:
        if os.path.exists("splash.png"):
            splash = QLabel()
            pixmap = QPixmap("splash.png")
            if not pixmap.isNull():
                splash.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio))
                splash.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
                splash.show()
                return splash
    except Exception as e:
        print(f"Splash screen error: {e}")
    return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Show splash screen
    splash = show_splash()
    
    # Create and show main window
    window = JARVISUI()
    window.show()
    
    # Close splash after delay if it exists
    if splash:
        QTimer.singleShot(2000, splash.close)
    
    sys.exit(app.exec_())