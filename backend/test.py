# backend/dmm.py
import re
from enum import Enum, auto
from typing import List, Dict, Tuple
import logging

class CommandType(Enum):
    GENERAL = auto()
    REALTIME = auto()
    OPEN = auto()
    CLOSE = auto()
    PLAY = auto()
    GENERATE_IMAGE = auto()
    REMINDER = auto()
    SYSTEM = auto()
    CONTENT = auto()
    YOUTUBE_SEARCH = auto()
    GOOGLE_SEARCH = auto()
    ECOMMERCE = auto()
    PORTFOLIO = auto()
    EXIT = auto()
    CODE_GENERATION = auto()
    EMAIL = auto()
    BROWSER = auto()

class FirstLayerDMM:
    def __init__(self):
        self.patterns = self._initialize_patterns()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _initialize_patterns(self) -> List[Dict]:
        return [
            # Exit commands (highest priority)
            {"regex": r'^(exit|quit|bye|stop)$', "type": CommandType.EXIT},
            
            # IP address queries
            {"regex": r'^(what is my|find my|check my|give me my|tell me my)\s+ip\s*(?:address)?\??$', "type": CommandType.REALTIME},
            {"regex": r'^ip\s*(?:address)?\??$', "type": CommandType.REALTIME},
            {"regex": r'^search\s+(?:on\s+)?google\s+(?:for\s+)?(.+)$', "type": CommandType.REALTIME},
            {"regex": r'^(who is|what is|do you know|can you find|i need|i want|how to|what was|who was|where is|define|teach me|research)\s+(.+)$', "type": CommandType.REALTIME},
            {"regex": r'^search\s+(?:for\s+)?(.+)$', "type": CommandType.REALTIME},
            # Temperature queries
            {"regex": r'^(what is|check|tell me)\s+(?:the\s+)?(temperature|temprature)\s*(?:outside|here)?\??$', "type": CommandType.REALTIME},
            {"regex": r'^(temperature|temprature)\s*(?:outside|here)?\??$', "type": CommandType.REALTIME},
            
            # Internet speed tests
            {"regex": r'^(check|test)\s+(?:internet\s+)?speed\??$', "type": CommandType.REALTIME},
            {"regex": r'^speed\s+test\??$', "type": CommandType.REALTIME},
            
            # Time/date queries (including Hindi)
            {"regex": r'^(what\'?s?|what is|current|latest)\s+(?:the\s+)?(time|date)\??\s*$', "type": CommandType.REALTIME},
            {"regex": r'^(tell|show)\s+me\s+(?:the\s+)?(time|date)', "type": CommandType.REALTIME},
            {"regex": r'^(time|samay|wagt)\s*(kya\s+hai|kitna\s+hua)\??$', "type": CommandType.REALTIME},
            
            # Weather queries
            {"regex": r'^(what\'?s?|what is|current|latest)\s+(?:the\s+)?weather\s*(?:in\s*(.+?))?\??\s*$', "type": CommandType.REALTIME},
            {"regex": r'^(tell|show)\s+me\s+(?:the\s+)?weather', "type": CommandType.REALTIME},
            
            # Price/stock queries
            {"regex": r'^(what\'?s?|what is)\s+(?:the\s+)?(price|value|stock\s*price)\s+(?:of\s+)?(.+?)\??\s*$', "type": CommandType.REALTIME},
            {"regex": r'^(how\s+much\s+is|check\s+price)\s+(?:the\s+)?(.+?)\??\s*$', "type": CommandType.REALTIME},
            {"regex": r'^(price|stock\s*price)\s+(?:of\s+)?(.+?)\??\s*$', "type": CommandType.REALTIME},
            
            # Email commands
            {"regex": r'^(send|compose)\s+(?:an?\s+)?(email|mail|gmail)\s*(?:about|regarding)?\s*(.+)?$', "type": CommandType.EMAIL},
            {"regex": r'^import\s+(?:emails?|gmails?)\??$', "type": CommandType.EMAIL},
            
            # Application control
            {"regex": r'^(open|launch|start|kholo)\s+(.+?)(?:\s+and\s+(.+))?$', "type": CommandType.OPEN},
            {"regex": r'^(close|shut\s+down|stop|band\s+karo)\s+(.+?)(?:\s+and\s+(.+))?$', "type": CommandType.CLOSE},
            
            # Browser commands
            {"regex": r'^(scroll|navigate)\s+(up|down|top|bottom)\??$', "type": CommandType.BROWSER},
            {"regex": r'^(new|open)\s+tab\??$', "type": CommandType.BROWSER},
            {"regex": r'^close\s+tab\??$', "type": CommandType.BROWSER},
            {"regex": r'^(reload|refresh)\s*(?:page|it)?\??$', "type": CommandType.BROWSER},
            
            # Volume control (including Hindi)
            {"regex": r'^(increase|decrease|set|mute|unmute)\s+(?:the\s+)?(volume|sound)\s*(?:to\s*(.+))?$', "type": CommandType.SYSTEM},
            {"regex": r'^(volume|sound)\s+(up|down|off|on|badhao|kam\s+karo)\??$', "type": CommandType.SYSTEM},
            
            # Media control
            {"regex": r'^(play|stream)\s+(.+?)(?:\s+on\s+(.+))?$', "type": CommandType.PLAY},
            {"regex": r'^start\s+(?:smart\s+)?music\s+system\??$', "type": CommandType.PLAY},
            
            # Content generation
            {"regex": r'^(generate|create|draw)\s+(?:an?|the)?\s*(image|picture|photo|art)\s+(?:of|about)?\s*(.+)$', "type": CommandType.GENERATE_IMAGE},
            {"regex": r'^(write|create|compose|generate|make)\s+(?:a|some)?\s*(content|blog|article|post|contect|articel)\s+(?:about|on|for)?\s*(.+)$', "type": CommandType.CONTENT},
            {"regex": r'^post\s+(?:a\s+)?(.+?)\s+blog\s*(?:in\s+website)?$', "type": CommandType.CONTENT},
            {"regex": r'^its time to post in website about (.+)$', "type": CommandType.CONTENT},
            {"regex": r'^(store|save)\s+(?:this|the)?\s*(article|blog)\s*(?:for website)?$', "type": CommandType.CONTENT},
            
            # Code generation
            {"regex": r'^(generate|create|write)\s+(?:a\s+)?(code|script|program|plugin)\s+(?:for\s+)?(.+)$', "type": CommandType.CODE_GENERATION},
            {"regex": r'^(make|build|develop)\s+(?:a\s+)?(python\s+)?script\s+(?:for\s+)?(.+)$', "type": CommandType.CODE_GENERATION},
            
            # Reminders and alerts
            {"regex": r'^(?:set\s+)?(?:a\s+)?reminder\s+(?:for|about|on)?\s*(.+)$', "type": CommandType.REMINDER},
            {"regex": r'^remind\s+me\s+(?:to|about)\s*(.+)$', "type": CommandType.REMINDER},
            
            # Search operations
            {"regex": r'^search\s+(?:on\s+)?google\s+(?:for\s+)?(.+)$', "type": CommandType.GOOGLE_SEARCH},
            {"regex": r'^search\s+(?:on\s+)?youtube\s+(?:for\s+)?(.+)$', "type": CommandType.YOUTUBE_SEARCH},
            {"regex": r'^(who is|what is|do you know|can you find|i need|i want|how to|what was|who was|where is|define|teach me|research)\s+(.+)$', "type": CommandType.GOOGLE_SEARCH},
            
            # E-commerce specific
            {"regex": r'^(order|buy|purchase)\s+(?:a\s+)?(.+)$', "type": CommandType.ECOMMERCE},
            
            # Portfolio specific
            {"regex": r'^(show|display)\s+(?:my\s+)?(portfolio|projects|work)\s*(.+)?$', "type": CommandType.PORTFOLIO},
            
            # System operations
            {"regex": r'^(shutdown|restart)\s+(?:my\s+)?(computer|system)', "type": CommandType.SYSTEM},
            {"regex": r'^(lock\s+screen|log\s+off|sleep)\??$', "type": CommandType.SYSTEM},
            
            # Default fallback (lowest priority)
            {"regex": r'^(.+)$', "type": CommandType.GENERAL}
        ]

    def categorize_query(self, user_input: str) -> str:
        """Categorize user input according to defined patterns"""
        clean_input = re.sub(r'\s+', ' ', user_input).strip().lower()
        self.logger.debug(f"Processing input: {clean_input}")
        
        # Check for compound commands first
        if ' and ' in clean_input or ', ' in clean_input:
            return self._handle_compound_command(clean_input)
            
        return self._categorize_single_command(clean_input)

    def _handle_compound_command(self, command: str) -> str:
        """Handle compound commands by splitting and categorizing each part"""
        # Normalize separators
        command = re.sub(r'\s*,\s*', ' and ', command)
        
        parts = re.split(r'\s+and\s+', command)
        categorized = []
        
        for part in parts:
            if part.strip():
                # Handle language-specific commands
                part = self._normalize_language_mix(part)
                categorized.append(self._categorize_single_command(part.strip()))
                
        return ' and '.join(categorized)

    def _normalize_language_mix(self, text: str) -> str:
        """Normalize Hindi/English mixed commands"""
        replacements = {
            'kholo': 'open',
            'band karo': 'close',
            'samay': 'time',
            'wagt': 'time',
            'volume badhao': 'increase volume',
            'volume kam karo': 'decrease volume',
            'back karo': 'go back',
            'undo karo': 'undo'
        }
        
        for hindi, english in replacements.items():
            text = text.replace(hindi, english)
        
        return text

    def _categorize_single_command(self, command: str) -> str:
        """Categorize a single command"""
        for pattern in self.patterns:
            match = re.match(pattern["regex"], command, re.IGNORECASE)
            if match:
                cmd_type = pattern["type"]
                payload = self._extract_payload(match, cmd_type)
                self.logger.debug(f"Matched pattern: {pattern['regex']} with type {cmd_type}")
                return f"{cmd_type.name.lower()} {payload}" if payload else cmd_type.name.lower()
        
        self.logger.debug("No specific pattern matched, using GENERAL")
        return CommandType.GENERAL.name.lower()

    def _extract_payload(self, match: re.Match, cmd_type: CommandType) -> str:
        """Extract the relevant payload from the match"""
        groups = match.groups()
        if not groups:
            return ""
            
        if cmd_type == CommandType.REALTIME:
            if 'ip' in match.re.pattern:
                return 'ip_address'
            elif 'temperature' in match.re.pattern:
                return 'temperature'
            elif 'speed' in match.re.pattern:
                return 'internet_speed'
            elif 'price' in match.re.pattern or 'value' in match.re.pattern or 'how much' in match.re.pattern:
                return groups[-1].rstrip('?')
            elif len(groups) > 1 and groups[-1]:
                return groups[-1]
            return groups[-2] if len(groups) > 1 else ""
            
        elif cmd_type in [CommandType.OPEN, CommandType.CLOSE, CommandType.BROWSER]:
            return groups[1] if len(groups) > 1 else ""
            
        elif cmd_type == CommandType.PLAY:
            return groups[1]
            
        elif cmd_type in [CommandType.GENERATE_IMAGE, CommandType.CONTENT, CommandType.CODE_GENERATION]:
            return groups[-1]
            
        elif cmd_type == CommandType.REMINDER:
            return groups[-1]
            
        elif cmd_type in [CommandType.GOOGLE_SEARCH, CommandType.YOUTUBE_SEARCH]:
            return groups[-1]
            
        elif cmd_type == CommandType.ECOMMERCE:
            return groups[-1]
            
        elif cmd_type == CommandType.PORTFOLIO:
            return groups[-1] if groups[-1] else ""
            
        elif cmd_type in [CommandType.SYSTEM, CommandType.EMAIL]:
            return groups[-1] if len(groups) > 1 else ""
            
        return groups[0]


if __name__ == "__main__":
    dmm = FirstLayerDMM()
    
    # Comprehensive test cases covering all command types
    test_cases = [
        # Exit commands
        ("exit", "exit"),
        ("quit", "exit"),
        
        # IP address
        ("what is my ip", "realtime ip_address"),
        ("ip address", "realtime ip_address"),
        
        # Temperature
        ("check temperature", "realtime temperature"),
        ("temprature outside", "realtime temperature"),
        
        # Internet speed
        ("check internet speed", "realtime internet_speed"),
        ("speed test", "realtime internet_speed"),
        
        # Time/date (including Hindi)
        ("what's the time", "realtime time"),
        ("samay kya hai", "realtime time"),
        
        # Weather
        ("what is the weather", "realtime"),
        ("tell me the weather in london", "realtime london"),
        
        # Price/stock
        ("what's the price of bitcoin", "realtime bitcoin"),
        ("stock price AAPL", "realtime aapl"),
        
        # Email
        ("send email to john", "email john"),
        ("import gmail", "email"),
        
        # Application control
        ("open chrome", "open chrome"),
        ("band karo spotify", "close spotify"),
        
        # Browser commands
        ("scroll down", "browser down"),
        ("new tab", "browser"),
        
        # Volume control
        ("increase volume", "system volume"),
        ("volume badhao", "system increase volume"),
        
        # Media
        ("play bohemian rhapsody", "play bohemian rhapsody"),
        ("start music system", "play"),
        
        # Content generation
        ("write a blog about AI", "content ai"),
        ("post data science blog", "content data science"),
        ("store this article", "content article"),
        
        # Code generation
        ("generate code for plugin", "code_generation plugin"),
        ("make python script for web scraping", "code_generation web scraping"),
        
        # Reminders
        ("set reminder for meeting", "reminder meeting"),
        
        # Search
        ("search on google for python", "google_search python"),
        ("how to make pizza", "google_search make pizza"),
        
        # E-commerce
        ("order a laptop", "ecommerce laptop"),
        
        # Portfolio
        ("show my portfolio", "portfolio"),
        
        # System
        ("shutdown computer", "system computer"),
        ("lock screen", "system"),
        
        # Compound commands
        ("open chrome and check weather", "open chrome and realtime"),
        ("play music and set reminder", "play music and reminder")
    ]

    print("Testing FirstLayerDMM:")
    print("=" * 60)
    for query, expected in test_cases:
        result = dmm.categorize_query(query)
        status = "✓" if result == expected else f"✗ (expected {expected})"
        print(f"{status} Input: '{query}'")
        print(f"   Output: {result}")
        print("-" * 60)

    # Interactive testing
    print("\nInteractive testing mode (type 'exit' to quit):")
    print("=" * 60)
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Goodbye!")
                break
                
            result = dmm.categorize_query(user_input)
            print(f"Category: {result}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")