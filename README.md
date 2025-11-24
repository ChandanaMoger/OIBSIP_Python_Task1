
#  Python Voice Assistant

A smart, cross-platform voice assistant that listens to your commands and speaks back! Built with Python for seamless voice interaction.

## Features

  - **Voice Recognition** - Listens and understands your commands
  - **Text-to-Speech** - Speaks responses using multiple TTS engines
  - **Time & Date** - Tells current time and date on command
  - **Web Search** - Opens Google search in your browser
  - **Cross-Platform** - Works on Windows, macOS, and Linux
  - **Simple Commands** - Easy-to-use voice interface

## Quick Start

### Installation & Run

```bash
# Save as voice_assistant.py and run:
python voice_assistant.py

# The program will automatically install dependencies!
```

### Try These Commands:
  
    "Hello" - Greets you
    "What time is it? - Tells current time  
    "What's the date?" - Tells today's date
    "Search Python" - Opens web search
    "How are you? - Chat response
    "Goodbye" - Exits program

## Tech Stack
   
   - **Python 3.6+** - Core language
   - **speech_recognition** - Voice input processing
   - **pyttsx3** - Text-to-speech engine
   - **Google Speech API** - Cloud-based recognition
   - **System TTS** - Native OS voice synthesis

## How It Works

1. **Listens** to your voice through microphone
2. **Processes** speech using Google's API
3. **Understands** commands with keyword matching
4. **Speaks** responses using best available TTS method
5. **Performs** actions like web search or time telling

##  Key Components

### Voice Recognition
- Real-time audio processing
- Noise cancellation
- Google API integration
- Error handling

### Multi-Platform TTS
- **Windows**: PowerShell & VBScript
- **macOS**: Native `say` command  
- **Linux**: `espeak` & `spd-say`
- **Universal**: pyttsx3 fallback

### Command Processing
- Natural language understanding
- Context-aware responses
- Extensible architecture

## Outcome

 - **Fully Functional** - Responds to all basic commands  
 - **Cross-Platform** - Consistent performance across OS  
 - **Reliable TTS** - Multiple fallback methods  
 - **Easy Setup** - Automatic dependency installation  
 - **Educational** - Clean, documented code

## Contributing

Want to enhance this project? Feel free to:
- Add new voice commands
- Improve natural language processing  
- Integrate with external APIs
- Create a GUI interface

*Happy coding! *
