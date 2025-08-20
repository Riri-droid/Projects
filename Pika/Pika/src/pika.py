import speech_recognition as sr
import pyttsx3
import pyautogui
import subprocess
import time
import os

class Pika:
    def __init__(self):
        # Initialize the recognizer
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Set a comfortable speaking rate
        self.engine.setProperty("rate", 150)
        
        print("Initializing Pika Voice Assistant...")
        self.speak("Pika is ready to assist you.")

    def listen(self):
        """Listen for voice commands"""
        with sr.Microphone() as source:
            print("Listening...")
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Listen for audio
            audio = self.recognizer.listen(source)
            
        try:
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, speech service is unavailable. Check your internet connection.")
            return ""

    def speak(self, text):
        """Convert text to speech"""
        print(f"Pika: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def open_notepad(self):
        """Open Notepad application"""
        try:
            subprocess.Popen("notepad.exe")
            time.sleep(1)  # Wait for Notepad to open
            return True
        except Exception as e:
            print(f"Error opening Notepad: {e}")
            return False

    def write_to_notepad(self, text):
        """Write text to Notepad"""
        if "write this:" in text:
            # Extract the text to write
            content = text.split("write this:", 1)[1].strip()
            
            # Check if Notepad is already open, if not open it
            if not self.is_notepad_open():
                self.open_notepad()
                
            # Type the text
            pyautogui.write(content)
            self.speak(f"I have written: {content}")
        else:
            self.speak("Please tell me what to write using the command 'Write this: your text'")

    def read_from_notepad(self):
        """Read text from Notepad"""
        # Make sure Notepad is in focus
        if not self.is_notepad_open():
            self.speak("Notepad is not open.")
            return
            
        # Select all text (Ctrl+A)
        pyautogui.hotkey("ctrl", "a")
        # Copy text (Ctrl+C)
        pyautogui.hotkey("ctrl", "c")
        
        # Wait a moment for the clipboard to update
        time.sleep(0.1)
        
        try:
            # Get clipboard content
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()  # Hide the tk window
            clipboard_text = root.clipboard_get()
            root.destroy()
            
            if clipboard_text.strip():
                self.speak("Here is the text in Notepad:")
                self.speak(clipboard_text)
            else:
                self.speak("Notepad is empty.")
        except Exception as e:
            print(f"Error reading clipboard: {e}")
            self.speak("I could not read the text in Notepad.")

    def is_notepad_open(self):
        """Check if Notepad is open"""
        try:
            # For Windows
            output = subprocess.check_output('tasklist /FI "IMAGENAME eq notepad.exe"', shell=True).decode()
            return "notepad.exe" in output
        except:
            return False

    def run(self):
        """Main loop for the assistant"""
        running = True
        self.speak("How can I help you today?")
        
        while running:
            command = self.listen()
            
            if "exit" in command or "quit" in command or "goodbye" in command:
                self.speak("Goodbye! Have a nice day.")
                running = False
                
            elif "write this:" in command:
                self.write_to_notepad(command)
                
            elif "read" in command:
                self.read_from_notepad()
                
            elif "open notepad" in command:
                self.open_notepad()
                self.speak("I have opened Notepad for you.")
                
            elif "hello" in command or "hi" in command:
                self.speak("Hello! I am Pika, your voice assistant.")
                
            elif command:  # If we have a command but no matching action
                self.speak("I'm not sure how to help with that. You can ask me to write text, read text, or open Notepad.")

def main():
    pika = Pika()
    try:
        pika.run()
    except KeyboardInterrupt:
        print("\nPika voice assistant terminated.")

if __name__ == "__main__":
    main()
