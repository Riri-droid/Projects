import speech_recognition as sr
import pyttsx3
import pyautogui
import subprocess
import time
import os

class Pika:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        
        print("Initializing Pika Voice Assistant...")
        self.speak("Pika is ready to assist you.")

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)
            
        try:
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
        print(f"Pika: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def open_notepad(self):
        try:
            subprocess.Popen("notepad.exe")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error opening Notepad: {e}")
            return False

    def focus_notepad(self):
        try:
            import pygetwindow as gw
            notepad_windows = gw.getWindowsWithTitle("Notepad")
            if notepad_windows:
                notepad_windows[0].activate()
            time.sleep(0.5)
        except ImportError:
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.5)

    def write_to_notepad(self, text):
        if "write " in text:
            content = text.split("write ", 1)[1].strip()
            
            if not self.is_notepad_open():
                self.open_notepad()
            else:
                self.focus_notepad()
                
            pyautogui.write(content + "\n")
            self.speak(f"I have written: {content}")
        else:
            self.speak("Please tell me what to write using the command 'Write your text'")

    def backspace_notepad(self):
        if not self.is_notepad_open():
            self.speak("Notepad is not open.")
            return
            
        self.focus_notepad()
        pyautogui.hotkey('ctrl', 'shift', 'left')
        pyautogui.press('delete')
        self.speak("I have deleted the last word.")

    def clear_notepad(self):
        if not self.is_notepad_open():
            self.speak("Notepad is not open.")
            return
            
        self.focus_notepad()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        self.speak("I have cleared all text.")

    def read_from_notepad(self):
        if not self.is_notepad_open():
            self.speak("Notepad is not open.")
            return
            
        self.focus_notepad()
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.1)
        
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
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
        try:
            output = subprocess.check_output('tasklist /FI "IMAGENAME eq notepad.exe"', shell=True).decode()
            return "notepad.exe" in output
        except:
            return False

    def run(self):
        running = True
        self.speak("How can I help you today?")
        
        while running:
            command = self.listen()
            
            if "exit" in command or "quit" in command or "goodbye" in command:
                self.speak("Goodbye! Have a nice day.")
                running = False
                
            elif "write " in command:
                self.write_to_notepad(command)
                
            elif "read" in command:
                self.read_from_notepad()
                
            elif "backspace" in command or "back word" in command or "delete word" in command:
                self.backspace_notepad()
                
            elif "clear" in command or "clear all" in command:
                self.clear_notepad()
                
            elif "open notepad" in command:
                self.open_notepad()
                self.speak("I have opened Notepad for you.")
                
            elif "hello" in command or "hi" in command:
                self.speak("Hello! I am Pika, your voice assistant.")
                
            elif command:
                self.speak("I'm not sure how to help with that. You can ask me to write text, read text, backspace, clear, or open Notepad.")

def main():
    pika = Pika()
    try:
        pika.run()
    except KeyboardInterrupt:
        print("\nPika voice assistant terminated.")

if __name__ == "__main__":
    main()
