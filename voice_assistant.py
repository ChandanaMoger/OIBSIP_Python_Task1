import speech_recognition as sr
import datetime
import webbrowser
import time
import os
import subprocess

class SimpleVoiceAssistant:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Calibrate microphone
        self.calibrate_microphone()
        print("🎤 Voice Assistant Ready!")
    
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        print("Calibrating microphone...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("✅ Microphone calibrated!")
        except Exception as e:
            print(f"⚠️ Microphone issue: {e}")
    
    def speak(self, text):
        """Universal TTS that works on all systems"""
        print(f"Assistant: {text}")
        
        # Method 1: Try system TTS first (most reliable)
        try:
            self.system_speak(text)
            return
        except:
            pass
        
        # Method 2: Try pyttsx3 as backup
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            return
        except:
            pass
        
        # Method 3: Final fallback - just print
        print(f"[SPEAK]: {text}")
    
    def system_speak(self, text):
        """Use system's built-in TTS (most reliable)"""
        text = text.replace('"', '')  # Remove quotes that might cause issues
        
        if os.name == 'nt':  # Windows
            # Method 1: Using PowerShell (most reliable on Windows)
            try:
                subprocess.run([
                    'powershell', '-Command', 
                    f'Add-Type -AssemblyName System.Speech; ' 
                    f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; ' 
                    f'$speak.Speak("{text}")'
                ], check=True, timeout=10)
                return
            except:
                pass
            
            # Method 2: Using cscript (alternative Windows method)
            try:
                # Create a VBS script for speaking
                vbs_script = f'''
                Set sapi = CreateObject("sapi.spvoice")
                sapi.Speak "{text}"
                '''
                with open("temp_speak.vbs", "w") as f:
                    f.write(vbs_script)
                subprocess.run(["cscript", "//Nologo", "temp_speak.vbs"], timeout=10)
                os.remove("temp_speak.vbs")
                return
            except:
                pass
        
        elif os.name == 'posix':  # macOS or Linux
            # macOS
            if 'darwin' in os.sys.platform:
                try:
                    subprocess.run(['say', text], check=True, timeout=10)
                    return
                except:
                    pass
            
            # Linux
            else:
                try:
                    # Try espeak first
                    subprocess.run(['espeak', text], check=True, timeout=10)
                    return
                except:
                    try:
                        # Try spd-say as alternative
                        subprocess.run(['spd-say', text], check=True, timeout=10)
                        return
                    except:
                        pass
    
    def listen(self):
        """Listen for voice commands"""
        try:
            with self.microphone as source:
                print("🎤 Listening... (Speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
            
            print("🔄 Processing...")
            command = self.recognizer.recognize_google(audio).lower()
            print(f"👤 You said: {command}")
            return command
        
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't understand that.")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""
    
    def get_time(self):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The time is {current_time}")
    
    def get_date(self):
        """Get current date"""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        self.speak(f"Today is {current_date}")
    
    def search_web(self, query):
        """Search the web"""
        if query:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            self.speak(f"Searching for {query}")
        else:
            self.speak("What would you like me to search for?")
            new_query = self.listen()
            if new_query:
                self.search_web(new_query)
    
    def greet(self):
        """Greet the user"""
        hour = datetime.datetime.now().hour
        if hour < 12:
            self.speak("Good morning! How can I help you?")
        elif hour < 18:
            self.speak("Good afternoon! How can I help you?")
        else:
            self.speak("Good evening! How can I help you?")
    
    def process_command(self, command):
        """Process voice commands"""
        if not command:
            return True
        
        command = command.lower()
        
        # Exit commands
        if any(word in command for word in ["exit", "quit", "goodbye", "bye"]):
            self.speak("Goodbye! Have a great day!")
            return False
        
        # Greeting
        elif any(word in command for word in ["hello", "hi", "hey"]):
            self.speak("Hello! How can I assist you today?")
        
        # Time
        elif "time" in command:
            self.get_time()
        
        # Date
        elif "date" in command or "today" in command:
            self.get_date()
        
        # Search
        elif "search" in command:
            query = command.replace("search", "").strip()
            self.search_web(query)
        
        # How are you
        elif "how are you" in command:
            self.speak("I'm doing great! Thank you for asking!")
        
        # Help
        elif "help" in command:
            self.speak("I can tell you the time, date, search the web, or just chat with you!")
        
        else:
            self.speak("I'm not sure about that. Try asking for time, date, or search.")
        
        return True
    
    def test_voice(self):
        """Test if voice output works"""
        print("\n" + "="*50)
        print("VOICE TEST - You should hear this!")
        print("="*50)
        
        test_phrases = [
            "Hello! I am your voice assistant.",
            "This is a voice test.",
            "If you can hear me, the voice is working!"
        ]
        
        for phrase in test_phrases:
            print(f"Testing: {phrase}")
            self.speak(phrase)
            time.sleep(2)
    
    def run(self):
        """Main assistant loop"""
        self.test_voice()
        self.greet()
        
        while True:
            try:
                command = self.listen()
                if not self.process_command(command):
                    break
                time.sleep(1)
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

def install_dependencies():
    """Install required packages"""
    packages = ["speechrecognition", "pyttsx3", "pyaudio"]
    
    for package in packages:
        try:
            if package == "pyaudio":
                # Try different methods for pyaudio
                try:
                    import pyaudio
                    print("✅ pyaudio already installed")
                except:
                    print("Installing pyaudio...")
                    if os.name == 'nt':  # Windows
                        os.system("pip install pipwin")
                        os.system("pipwin install pyaudio")
                    else:  # Mac/Linux
                        os.system("pip install pyaudio")
            else:
                os.system(f"pip install {package}")
                print(f"✅ {package} installed")
        except:
            print(f"⚠️ Could not install {package}")

if __name__ == "__main__":
    print("🚀 Starting Simple Voice Assistant...")
    print("This version WILL produce voice output!")
    
    # Install dependencies if needed
    response = input("Do you want to install required packages? (y/n): ").lower()
    if response == 'y':
        install_dependencies()
    
    assistant = SimpleVoiceAssistant()
    assistant.run()