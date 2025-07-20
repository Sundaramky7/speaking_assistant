# from lib2to3.pgen2 import driver
# from multiprocessing import dummy
from gestures import gesture
from openApp import start
import colorama
import subprocess
# import sys
# import urllib
# from selenium import webdriver
# import bs4
# import requests
import urllib.request
import re
# from time import sleep
# from typing_extensions import runtime
import pyttsx3
import speech_recognition as sr
# import wolframalpha
import wikipedia
import webbrowser
import datetime
import os
import logging
from email_handler import email_handler
from contacts import contact_manager
# from instabot import Bot
# from twilio.rest import Client
# from cgi import parse_qs
# from ecapture import ecapture as ec
engine = pyttsx3.init()
# print(engine);
voices = engine.getProperty('voices')
# print(voices);
rate = engine.getProperty('rate')
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voice_assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

os.system("clear")
#For knowing the all voices Name and ID:
k=0
for n in range(0,len(voices)-1):
    # print(n,voices[n].name)
    if(voices[n].name=='Rishi'):
        k=n
        logger.info(f"Voice '{voices[n].name}' selected at index {n}")
engine.setProperty('voice',voices[k].id)
engine. setProperty("rate", 160)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
# def wishMe():
#     hour = int(datetime.datetime.now().hour)
#     if (hour>=0 and hour<12):
#         speak("Good Morning")
#     if hour>=12 and hour<18:
#         speak("Good afternoon")
#     if hour>=18 and hour<24:
#         speak("Good night")
speak("Hello , I am Rishi")
# print(colorama.Fore.GREEN+"+++++++ I am ",namea," +++++++"+colorama.Fore.RESET);
print(colorama.Fore.YELLOW+"+++++++ I am RISHI +++++++"+colorama.Fore.WHITE);

# Global recognizer for reuse
global_recognizer = sr.Recognizer()

def setup_recognizer():
    """
    Initialize and configure the speech recognizer with optimal settings
    """
    global global_recognizer
    
    # Optimized settings for faster and better recognition
    global_recognizer.energy_threshold = 4000  # Higher threshold for cleaner audio detection
    global_recognizer.dynamic_energy_threshold = True  # Automatically adjust energy threshold
    global_recognizer.pause_threshold = 0.5  # Shorter pause detection for faster response
    global_recognizer.phrase_threshold = 0.2  # Shorter minimum phrase duration
    global_recognizer.non_speaking_duration = 0.3  # Less non-speaking audio padding
    
    logger.info("Speech recognizer initialized with optimal settings")
    print(colorama.Fore.GREEN + "🎤 Speech recognizer initialized with optimal settings" + colorama.Fore.WHITE)

def calibrate_microphone():
    """
    Calibrate microphone for ambient noise levels
    """
    try:
        with sr.Microphone() as source:
            logger.info("Starting microphone calibration")
            print(colorama.Fore.CYAN + "🔧 Calibrating microphone for ambient noise..." + colorama.Fore.WHITE)
            global_recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Shorter calibration time
            logger.info("Microphone calibration completed successfully")
            print(colorama.Fore.GREEN + "✅ Microphone calibration complete" + colorama.Fore.WHITE)
    except Exception as e:
        logger.error(f"Microphone calibration failed: {e}")
        print(colorama.Fore.RED + f"❌ Microphone calibration failed: {e}" + colorama.Fore.WHITE)
        speak("Microphone calibration failed. Speech recognition may be less accurate.")

def tackcommand(max_retries=2, timeout=3):
    """
    Optimized speech recognition with better error handling and user feedback
    
    Args:
        max_retries (int): Maximum number of retry attempts
        timeout (int): Maximum seconds to wait for speech
    
    Returns:
        str: Recognized speech text or "None" if failed
    """
    global global_recognizer
    
    for attempt in range(max_retries):
        try:
            with sr.Microphone() as source:
                # Visual feedback with better spacing
                print("\n" + "="*50)
                if attempt == 0:
                    print(colorama.Fore.BLUE + "🎧 Listening..." + colorama.Fore.WHITE)
                else:
                    print(colorama.Fore.YELLOW + f"🔄 Retry {attempt}/{max_retries-1} - Listening..." + colorama.Fore.WHITE)
                print("="*50)
                
                # Listen for audio with timeout
                audio = global_recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
                
                # Recognition feedback
                print(colorama.Fore.MAGENTA + "\n🔍 Processing speech..." + colorama.Fore.WHITE)
                
                # Try Google Speech Recognition first
                try:
                    query = global_recognizer.recognize_google(audio, language='en-US')
                    logger.info(f"Speech recognized: '{query}'")
                    print(colorama.Fore.GREEN + f"\n✅ You said: '{query}'\n" + colorama.Fore.WHITE)
                    
                    # Confidence check (basic validation)
                    if len(query.strip()) > 0:
                        return query.strip()
                    else:
                        print(colorama.Fore.YELLOW + "⚠️ Empty response detected\n" + colorama.Fore.WHITE)
                        continue
                        
                except sr.UnknownValueError:
                    logger.warning("Could not understand audio input")
                    print(colorama.Fore.YELLOW + "\n⚠️ Could not understand audio\n" + colorama.Fore.WHITE)
                    if attempt < max_retries - 1:
                        continue
                    
                except sr.RequestError as e:
                    logger.error(f"Google Speech Recognition error: {e}")
                    print(colorama.Fore.RED + f"\n❌ Google Speech Recognition error: {e}\n" + colorama.Fore.WHITE)
                    
                    # Fallback to alternative recognition methods
                    try:
                        # Try with different language models
                        query = global_recognizer.recognize_google(audio, language='en-IN')
                        logger.info(f"Speech recognized with fallback: '{query}'")
                        print(colorama.Fore.GREEN + f"\n✅ (Fallback) You said: '{query}'\n" + colorama.Fore.WHITE)
                        return query.strip()
                    except:
                        if attempt < max_retries - 1:
                            continue
                        
        except sr.WaitTimeoutError:
            logger.warning(f"Listening timeout on attempt {attempt + 1}")
            print(colorama.Fore.YELLOW + "\n⏱️ Listening timeout - no speech detected\n" + colorama.Fore.WHITE)
            # Don't speak on timeout - just show visual feedback
            if attempt < max_retries - 1:
                continue
                
        except Exception as e:
            logger.error(f"Unexpected error in speech recognition: {e}")
            print(colorama.Fore.RED + f"\n❌ Unexpected error: {e}\n" + colorama.Fore.WHITE)
            if attempt < max_retries - 1:
                continue
    
    # All attempts failed
    logger.error("Speech recognition failed after all attempts")
    print(colorama.Fore.RED + "\n❌ Speech recognition failed after all attempts\n" + colorama.Fore.WHITE)
    return "None"

def quick_command():
    """
    Quick speech recognition for simple commands (shorter timeout)
    """
    return tackcommand(max_retries=1, timeout=2)

def long_command():
    """
    Extended speech recognition for longer inputs like email content
    """
    return tackcommand(max_retries=2, timeout=6)

def setup_email_configuration():
    """
    Setup email configuration on-demand when user tries to send email
    
    Returns:
        bool: True if setup completed successfully, False if cancelled
    """
    import getpass
    import re
    from pathlib import Path
    
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    try:
        print(colorama.Fore.CYAN + "\n" + "="*50)
        print("📧 EMAIL CONFIGURATION SETUP")
        print("="*50 + colorama.Fore.WHITE)
        
        # Get email address
        while True:
            email = input("Enter your email address: ").strip()
            
            if not email:
                print(colorama.Fore.RED + "❌ Email address is required!" + colorama.Fore.WHITE)
                continue
            
            if not validate_email(email):
                print(colorama.Fore.RED + "❌ Invalid email format!" + colorama.Fore.WHITE)
                continue
            
            break
        
        # Get email password
        while True:
            print(colorama.Fore.YELLOW + "\n🔒 Email Password" + colorama.Fore.WHITE)
            print("For Gmail, use an App Password (not your regular password)")
            print("Generate one at: https://myaccount.google.com/apppasswords")
            
            password = getpass.getpass("Enter your email password/app password: ").strip().replace(" ", "")
            
            if not password:
                print(colorama.Fore.RED + "❌ Password is required!" + colorama.Fore.WHITE)
                continue
            
            break
        
        # Optional: SMTP settings
        print(colorama.Fore.YELLOW + "\n⚙️ SMTP Configuration (Optional)" + colorama.Fore.WHITE)
        smtp_server = input(f"SMTP Server [smtp.gmail.com]: ").strip() or "smtp.gmail.com"
        smtp_port_input = input(f"SMTP Port [587]: ").strip()
        smtp_port = smtp_port_input if smtp_port_input.isdigit() else "587"
        
        # Remove all spaces from password before saving (not just leading/trailing)
        password = password.replace(" ", "")
        
        # Save configuration to .env file
        env_path = Path(__file__).parent / '.env'
        
        # Read existing .env content if it exists
        existing_content = ""
        if env_path.exists():
            with open(env_path, 'r') as f:
                existing_content = f.read()
        
        # Update or add email configuration
        lines = existing_content.split('\n') if existing_content else []
        updated_lines = []
        email_keys = {'EMAIL_ADDRESS', 'EMAIL_PASSWORD', 'SMTP_SERVER', 'SMTP_PORT'}
        found_keys = set()
        
        # Update existing lines
        for line in lines:
            if '=' in line and not line.strip().startswith('#'):
                key = line.split('=')[0].strip()
                if key == 'EMAIL_ADDRESS':
                    updated_lines.append(f"EMAIL_ADDRESS={email}")
                    found_keys.add('EMAIL_ADDRESS')
                elif key == 'EMAIL_PASSWORD':
                    updated_lines.append(f"EMAIL_PASSWORD={password}")
                    found_keys.add('EMAIL_PASSWORD')
                elif key == 'SMTP_SERVER':
                    updated_lines.append(f"SMTP_SERVER={smtp_server}")
                    found_keys.add('SMTP_SERVER')
                elif key == 'SMTP_PORT':
                    updated_lines.append(f"SMTP_PORT={smtp_port}")
                    found_keys.add('SMTP_PORT')
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        # Add missing email configuration
        if 'EMAIL_ADDRESS' not in found_keys:
            updated_lines.append(f"EMAIL_ADDRESS={email}")
        if 'EMAIL_PASSWORD' not in found_keys:
            updated_lines.append(f"EMAIL_PASSWORD={password}")
        if 'SMTP_SERVER' not in found_keys:
            updated_lines.append(f"SMTP_SERVER={smtp_server}")
        if 'SMTP_PORT' not in found_keys:
            updated_lines.append(f"SMTP_PORT={smtp_port}")
        
        # Write updated content
        with open(env_path, 'w') as f:
            f.write('\n'.join(updated_lines))
        
        # Update environment variables immediately
        import os
        os.environ['EMAIL_ADDRESS'] = email
        os.environ['EMAIL_PASSWORD'] = password
        os.environ['SMTP_SERVER'] = smtp_server
        os.environ['SMTP_PORT'] = smtp_port
        
        print(colorama.Fore.GREEN + f"\n✅ Email configuration saved to {env_path}" + colorama.Fore.WHITE)
        logger.info("Email configuration completed successfully")
        
        return True
        
    except KeyboardInterrupt:
        print(colorama.Fore.YELLOW + "\n⚠️ Email configuration cancelled" + colorama.Fore.WHITE)
        return False
    except Exception as e:
        print(colorama.Fore.RED + f"\n❌ Error during email setup: {e}" + colorama.Fore.WHITE)
        logger.error(f"Email configuration failed: {e}")
        return False
def allEmails(to, count):
    # Use the new find_or_add_contact method that prompts for new contacts
    email_address, contact_name = contact_manager.find_or_add_contact(to)
    if email_address:
        emailThings(email_address, contact_name)
    else:
        speak('Email cancelled or contact could not be added.')
def emailThings(to, name):
    speak("What should I say?")
    content = long_command()  # Use extended timeout for email content
    if content and content != "None":
        if email_handler.send_email(to, f"Email from voice assistant", content):
            speak(f"Email has been sent to {name}")
        else:
            speak("Failed to send email. Please check your configuration.")
    else:
        speak("Email content was not understood. Email not sent.")
def safe_open_browser(url, message=None, browser_name='chrome'):
    """Safely open a URL in browser with consistent error handling"""
    try:
        if message:
            speak(message)
        webbrowser.get(browser_name).open(url)
        logger.info(f"Successfully opened URL: {url}")
        return True
    except Exception as e:
        logger.error(f"Failed to open URL {url}: {e}")
        speak("Sorry, I couldn't open that webpage")
        return False

def safe_open_browser_tab(url, message=None, browser_name='chrome'):
    """Safely open a URL in new browser tab with consistent error handling"""
    try:
        if message:
            speak(message)
        webbrowser.get(browser_name).open_new_tab(url)
        logger.info(f"Successfully opened URL in new tab: {url}")
        return True
    except Exception as e:
        logger.error(f"Failed to open URL {url} in new tab: {e}")
        speak("Sorry, I couldn't open that webpage")
        return False

def print_colored_header(text, color=colorama.Fore.CYAN, symbol="📝"):
    """Print a consistently formatted colored header"""
    print("\n" + "-"*50)
    print(color + f"{symbol} {text}" + colorama.Fore.WHITE)
    print("-"*50)

def print_colored_info(text, color=colorama.Fore.GREEN, symbol="ℹ️"):
    """Print consistently formatted colored information"""
    print(color + f"{symbol} {text}" + colorama.Fore.WHITE)

def print_colored_error(text, symbol="❌"):
    """Print consistently formatted error messages"""
    print(colorama.Fore.RED + f"{symbol} {text}" + colorama.Fore.WHITE)

def print_colored_warning(text, symbol="⚠️"):
    """Print consistently formatted warning messages"""
    print(colorama.Fore.YELLOW + f"{symbol} {text}" + colorama.Fore.WHITE)

def clean_query(query, keywords_to_remove):
    """Clean query by removing specified keywords and extra whitespace"""
    result = query.lower().strip()
    for keyword in keywords_to_remove:
        result = result.replace(keyword, "").strip()
    return result

def execute_with_error_handling(func, query, operation_name):
    """Execute a function with consistent error handling and logging"""
    try:
        logger.info(f"{operation_name} initiated for query: '{query}'")
        result = func(query)
        logger.info(f"{operation_name} completed successfully")
        return result
    except Exception as e:
        logger.error(f"{operation_name} failed: {e}")
        print_colored_error(f"{operation_name} failed: {e}")
        speak(f"Sorry, {operation_name.lower()} failed. Please try again.")
        return None

def search_web(query):
    """Search the web using Google"""
    return safe_open_browser_tab(f'https://google.com/search?q={query}', "Searching the web")

def search_youtube(query):
    """Search for a video on YouTube"""
    def _search_youtube_internal(query):
        speak("Searching YouTube")
        html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query}")
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        if video_ids:
            video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
            print(video_url)
            return safe_open_browser(video_url)
        else:
            speak("No videos found")
            return False
    
    return execute_with_error_handling(_search_youtube_internal, query, "YouTube search")

# Command Handler Functions
def handle_wikipedia(query):
    """Handle Wikipedia search commands"""
    def _wikipedia_search(query):
        cleaned_query = clean_query(query, ["wikipedia"])
        if not cleaned_query:
            speak("What would you like to search for on Wikipedia?")
            return None
            
        print_colored_header("Searching Wikipedia", symbol="🔍")
        speak('Searching Wikipedia...')
        
        results = wikipedia.summary(cleaned_query, sentences=4)
        speak("According to Wikipedia")
        print_colored_info(f"Wikipedia Results for '{cleaned_query}':", symbol="📖")
        print("-"*30)
        print(results)
        print("-"*30 + "\n")
        speak(results)
        return True
    
    return execute_with_error_handling(_wikipedia_search, query, "Wikipedia search")

def handle_identity(query):
    """Handle identity questions"""
    print("I am Rishi")
    speak("I am Rishi")
    speak("a voice assistant")
    print("a voice assistant. I am programmed to do a couple of things like Opening apps, Browsing, Sending an email and Playing music.")

def handle_show_capabilities(query):
    """Show all available commands and capabilities (print only, no speech)"""
    print(colorama.Fore.CYAN + "\n" + "="*60)
    print("🎤 RISHI VOICE ASSISTANT - CAPABILITIES")
    print("="*60 + colorama.Fore.WHITE)
    
    capabilities = [
        (
            "🌐 WEB & SEARCH",
            [
                ("Open YouTube", "Opens YouTube website"),
                ("Open Google", "Opens Google homepage"),
                ("Open Stack Overflow", "Opens Stack Overflow for developers"),
                ("Search [query]", "Performs Google web search"),
                ("Search Google [query]", "Explicit Google search"),
                ("Search YouTube [query]", "Searches YouTube videos"),
                ("Wikipedia [topic]", "Gets Wikipedia information with audio"),
            ]
        ),
        (
            "📧 EMAIL & CONTACTS",
            [
                ("Send email", "Send email to contacts (voice + keyboard)"),
                ("Add contact", "Add new contact (voice name, keyboard email)"),
                ("List contacts", "Display all saved contacts"),
            ]
        ),
        (
            "🎵 MEDIA & ENTERTAINMENT",
            [
                ("Play music", "Opens Spotify web player"),
                ("Play song", "Music playback commands"),
            ]
        ),
        (
            "💻 SYSTEM CONTROL",
            [
                ("Shutdown", "Power down the system"),
                ("Restart", "Reboot the system"),
                ("Bluetooth on/off", "Control Bluetooth settings"),
                ("Bluetooth show/list", "List Bluetooth devices"),
                ("Scan WiFi", "Scan for available WiFi networks"),
            ]
        ),
        (
            "🖥️ APPLICATION MANAGEMENT",
            [
                ("Open [app name]", "Launch any installed application"),
                ("Close [app name]", "Terminate running application"),
                ("Show apps", "List all installed applications"),
            ]
        ),
        (
            "🤚 GESTURE CONTROLS",
            [
                ("Swipe left", "Navigate to left workspace (macOS)"),
                ("Swipe right", "Navigate to right workspace (macOS)"),
            ]
        ),
        (
            "🤖 ASSISTANT INFO",
            [
                ("What's your name?", "Assistant introduction"),
                ("Who are you?", "Detailed assistant information"),
                ("What can you do?", "Show this capabilities list"),
            ]
        ),
    ]
    
    for category, commands in capabilities:
        print(f"\n{colorama.Fore.YELLOW}{category}{colorama.Fore.WHITE}")
        print("-" * len(category.replace('🌐 ', '').replace('📧 ', '').replace('🎵 ', '').replace('💻 ', '').replace('🖥️ ', '').replace('🤚 ', '').replace('🤖 ', '')))
        
        for command, description in commands:
            print(f"  {colorama.Fore.GREEN}'{command}'{colorama.Fore.WHITE} - {description}")
    
    print(f"\n{colorama.Fore.CYAN}💡 USAGE TIPS:{colorama.Fore.WHITE}")
    print("─" * 15)
    print("• Speak clearly and at moderate pace")
    print("• Wait for the listening prompt before speaking")
    print("• Email addresses are entered via keyboard for accuracy")
    print("• You can cancel most operations with Ctrl+C")
    print("• Contact names support partial matching")
    
    print(f"\n{colorama.Fore.CYAN}🔧 SPECIAL FEATURES:{colorama.Fore.WHITE}")
    print("─" * 20)
    print("• Smart contact management with auto-add prompts")
    print("• Noise calibration for better speech recognition")
    print("• Fallback language support (EN-US → EN-IN)")
    print("• Comprehensive error handling and retry logic")
    print("• Persistent contact storage in contacts.json")
    print("• Secure email configuration via .env file")
    
    print(f"\n{colorama.Fore.MAGENTA}📱 EXAMPLE CONVERSATIONS:{colorama.Fore.WHITE}")
    print("─" * 25)
    print("🎤 You: 'Send email'")
    print("🤖 Rishi: 'Name the Receiver'")
    print("🎤 You: 'John Smith'")
    print("🤖 Rishi: [If contact exists] 'What should I say?'")
    print("🤖 Rishi: [If new contact] 'Contact not found. Add? (y/n)'")
    
    print("\n🎤 You: 'Search YouTube cooking tutorials'")
    print("🤖 Rishi: 'Searching YouTube' [Opens first video result]")
    
    print("\n🎤 You: 'Wikipedia artificial intelligence'")
    print("🤖 Rishi: 'Searching Wikipedia...' [Speaks summary]")
    
    print(f"\n{colorama.Fore.CYAN}" + "="*60)
    print("Ready to assist! Say any command to get started.")
    print("="*60 + colorama.Fore.WHITE + "\n")

def handle_open_youtube(query):
    """Handle opening YouTube"""
    speak("Here you go to Youtube")
    webbrowser.get('chrome').open("https://youtube.com")

def handle_open_google(query):
    """Handle opening Google"""
    speak("Here you go to Google")
    webbrowser.get('chrome').open("https://google.com")

def handle_open_stackoverflow(query):
    """Handle opening Stack Overflow"""
    speak("Here you go to Stack Over flow. Happy coding")
    webbrowser.get('chrome').open("https://stackoverflow.com")

def handle_search_general(query):
    """Handle general search commands"""
    query = query.replace("search", "").strip()
    if 'youtube' in query:
        query = query.replace("in youtube", '').strip()
        if query:
            search_youtube(query)
        else:
            speak("What would you like to search for on YouTube?")
    else:
        if query:
            search_web(query)
        else:
            speak("What would you like to search for?")

def handle_play_music(query):
    """Handle music playing commands"""
    if 'play song' in query or 'play music' in query:
        speak("Here we go to spotify website")
        webbrowser.get('chrome').open_new_tab('https://open.spotify.com')
    else:
        speak("What would you like to play?")

def handle_send_email(query):
    """Handle email sending commands with on-demand email configuration"""
    logger.info("Email sending initiated")
    
    # First check if email is configured
    from config import config
    if not config.is_email_configured():
        print(colorama.Fore.YELLOW + "\n📧 Email Configuration Required" + colorama.Fore.WHITE)
        speak("Email is not configured. Let me help you set it up.")
        
        # Run email setup
        if setup_email_configuration():
            speak("Email configuration completed. Now let's send your email.")
        else:
            speak("Email configuration was cancelled. Cannot send email.")
            return
    
    try:
        speak("Name the Receiver")
        to = tackcommand()
        if to != "None":
            logger.info(f"Email receiver identified: {to}")
            count = len(to.replace(' ', ''))
            allEmails(to.lower(), count)
        else:
            logger.warning("Could not understand receiver name")
            speak("Could not understand the receiver name")
    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        print(e)
        speak("I am not able to send this email")

def handle_list_contacts(query):
    """Handle listing contacts"""
    contact_manager.list_contacts()

def handle_add_contact(query):
    """Handle adding new contacts via voice for name, keyboard for email"""
    logger.info("Add contact initiated")
    try:
        speak("What is the contact's name?")
        name = tackcommand()
        if name != "None":
            # Use keyboard input for email address
            print(colorama.Fore.CYAN + "\n📧 Email Input Required" + colorama.Fore.WHITE)
            speak("Please type the email address on your keyboard")
            
            while True:
                try:
                    email = input(f"Enter email address for {name}: ").strip()
                    
                    if not email:
                        print(colorama.Fore.RED + "❌ Email address is required!" + colorama.Fore.WHITE)
                        speak("Email address is required. Please try again.")
                        continue
                    
                    # Validate email format
                    if contact_manager.validate_email(email):
                        contact_manager.add_contact(name, email)
                        speak(f"Contact {name} has been added successfully with email {email}")
                        print(colorama.Fore.GREEN + f"✅ Contact '{name}' added successfully!" + colorama.Fore.WHITE)
                        break
                    else:
                        print(colorama.Fore.RED + "❌ Invalid email format!" + colorama.Fore.WHITE)
                        speak("That's not a valid email format. Please try again.")
                        continue
                        
                except KeyboardInterrupt:
                    print(colorama.Fore.YELLOW + "\n⚠️ Contact addition cancelled" + colorama.Fore.WHITE)
                    speak("Contact addition cancelled")
                    return
        else:
            speak("I couldn't understand the contact name")
    except Exception as e:
        logger.error(f"Add contact failed: {e}")
        speak("I couldn't add the contact. Please try again.")

def handle_shutdown(query):
    """Handle system shutdown"""
    speak("ok, i gona sleep")
    subprocess.call(["shutdown", "/s"])

def handle_restart(query):
    """Handle system restart"""
    speak("ok, i will be restarting now")
    subprocess.call(["shutdown", "/r"])

def handle_bluetooth(query):
    """Handle Bluetooth commands"""
    if 'off' in query:
        os.system("blueutil -p 0")
        speak("Bluetooth is turned off")
        print("Bluetooth is turned off")
    elif 'on' in query:
        os.system("blueutil -p 1")
        speak("Bluetooth is turned on")
        print("Bluetooth is turned on")
    elif 'show' in query or 'list' in query:
        speak("These are the available bluetooth devices")
        os.system("system_profiler SPBluetoothDataType")

def handle_wifi_scan(query):
    """Handle WiFi scanning"""
    speak("Scanning for available WiFi networks")
    print("These are the available wifi devices:")
    wlan()

def handle_gesture(query):
    """Handle gesture commands"""
    gesture(query)

def handle_app_control(query):
    """Handle app control commands (open/close/show)"""
    start(query)

# Command mapping dictionary
COMMAND_HANDLERS = {
    # Search commands
    'wikipedia': handle_wikipedia,
    'search google': lambda q: search_web(q.replace('search google', '').strip()),
    'search youtube': lambda q: search_youtube(q.replace('search youtube', '').strip()),
    'search': handle_search_general,
    
    # Identity commands
    'what your name': handle_identity,
    'who are you': handle_identity,
    'what can you do': handle_show_capabilities,
    
    # Web browsing
    'open youtube': handle_open_youtube,
    'open google': handle_open_google,
    'open stack overflow': handle_open_stackoverflow,
    
    # Media
    'play': handle_play_music,
    
    # Email
    'send email': handle_send_email,
    'list contacts': handle_list_contacts,
    'add contact': handle_add_contact,
    
    # System control
    'shutdown': handle_shutdown,
    'restart': handle_restart,
    
    # Bluetooth and WiFi
    'bluetooth': handle_bluetooth,
    'scan wi-fi': handle_wifi_scan,
    'scan wifi': handle_wifi_scan,
    
    # Gestures
    'swipe': handle_gesture,
    
    # App control (catch-all for open/close/show commands)
    'close': handle_app_control,
    'open': handle_app_control,
    'show': handle_app_control,
}

def parse_command(query):
    """Parse user query and find matching command handler"""
    query = query.lower().strip()
    
    # Sort commands by length (longest first) to handle overlapping patterns
    sorted_commands = sorted(COMMAND_HANDLERS.keys(), key=len, reverse=True)
    
    for command_pattern in sorted_commands:
        if command_pattern in query:
            handler = COMMAND_HANDLERS[command_pattern]
            return handler, query
    
    return None, query

def handle_unknown_command(query):
    """Handle unknown commands"""
    logger.warning(f"Unknown command received: '{query}'")
    speak("I'm sorry, I don't understand that command. Please try again.")
    print(colorama.Fore.YELLOW + f"⚠️ Unknown command: {query}" + colorama.Fore.WHITE)

# def scan():
    
#     print("Scanning for bluetooth devices:")

#     devices = blotuth.discover_devices()

#     number_of_devices = len(devices)

#     print(number_of_devices,"devices found")

#     for addr, name, device_class in devices:

#         print("\n")

#         print("Device:")

#         print("Device Name: %s" % (name))

#         print("Device MAC Address: %s" % (addr))

#         print("Device Class: %s" % (device_class))

#         print("\n")

#     return

def wlan():
    os.system("airport -s")


if __name__ == '__main__':
    # Initialize speech recognition with optimized settings
    setup_recognizer()
    calibrate_microphone()
    
    # speak("hello  I am Edith Tony's augmented reality secuirty and defense system so you have all Tony's protocols")
    # speak("Edith stand for Eden dead I'm the hero")
    # youtubeSearch()
    
    logger.info("Voice assistant initialization complete")
    speak("Speech recognition optimized and ready!")
    print(colorama.Fore.GREEN + "\n🚀 Voice Assistant Ready - Say something!" + colorama.Fore.WHITE)
    print("\n" + "*"*60)
    print(colorama.Fore.CYAN + "               VOICE ASSISTANT ACTIVE" + colorama.Fore.WHITE)
    print("*"*60 + "\n")
    
    while True:
        query = tackcommand().lower()
        
        # Skip processing if no valid query
        if query == "none":
            continue
        # chromeAddres = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        braveAddres = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser";
        webbrowser.register('brave',None,webbrowser.BackgroundBrowser(braveAddres))
        
        #Web Automation code:
        # driver = webdriver.Safari()        
        # Logic for executive tasks based on query
        print("\n" + "-"*50)
        print(colorama.Fore.CYAN + f"📝 Processing command: {query}" + colorama.Fore.WHITE)
        print("-"*50)
        
        # Use new command parsing system
        handler, parsed_query = parse_command(query)
        
        if handler:
            try:
                logger.info(f"Executing command: '{query}'")
                handler(parsed_query)
                logger.info(f"Command executed successfully: '{query}'")
            except Exception as e:
                logger.error(f"Error executing command '{query}': {e}")
                print(colorama.Fore.RED + f"❌ Error executing command: {e}" + colorama.Fore.WHITE)
                speak("Sorry, there was an error processing your command.")
        else:
            handle_unknown_command(query)
        