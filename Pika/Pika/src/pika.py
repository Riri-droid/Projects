import speech_recognition as sr
import pyttsx3
import pyautogui
import subprocess
import time
import os
import json
import datetime
from difflib import SequenceMatcher
import pickle

class Pika:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        
        # AI Learning components
        self.command_history = []
        self.user_preferences = {}
        self.command_patterns = {}
        self.context_memory = {}
        self.load_learning_data()
        
        print("Initializing Pika AI Voice Assistant...")
        self.speak("Pika AI is ready to assist and learn from you.")

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

    def load_learning_data(self):
        """Load AI learning data from files"""
        try:
            with open("pika_learning.json", "r") as f:
                data = json.load(f)
                self.command_history = data.get("command_history", [])
                self.user_preferences = data.get("user_preferences", {})
                self.command_patterns = data.get("command_patterns", {})
                self.context_memory = data.get("context_memory", {})
        except FileNotFoundError:
            print("No existing learning data found. Starting fresh.")

    def save_learning_data(self):
        """Save AI learning data to files"""
        data = {
            "command_history": self.command_history[-100:], 
            "user_preferences": self.user_preferences,
            "command_patterns": self.command_patterns,
            "context_memory": self.context_memory
        }
        with open("pika_learning.json", "w") as f:
            json.dump(data, f, indent=2)

    def learn_from_command(self, command, action_taken):
        """Learn from user commands and actions"""
        timestamp = datetime.datetime.now().isoformat()
        
     
        self.command_history.append({
            "command": command,
            "action": action_taken,
            "timestamp": timestamp
        })
        
        
        if action_taken not in self.command_patterns:
            self.command_patterns[action_taken] = []
        self.command_patterns[action_taken].append(command)
        
       
        hour = datetime.datetime.now().hour
        if hour not in self.context_memory:
            self.context_memory[hour] = {}
        if action_taken not in self.context_memory[hour]:
            self.context_memory[hour][action_taken] = 0
        self.context_memory[hour][action_taken] += 1
        
        self.save_learning_data()

    def predict_intent(self, command):
        """Use AI to predict user intent from command"""
        best_match = None
        best_score = 0
        
        for action, patterns in self.command_patterns.items():
            for pattern in patterns:
                similarity = SequenceMatcher(None, command.lower(), pattern.lower()).ratio()
                if similarity > best_score and similarity > 0.6:  
                    best_score = similarity
                    best_match = action
        
        return best_match, best_score

    def get_contextual_suggestions(self):
        """Provide contextual suggestions based on time and usage patterns"""
        current_hour = datetime.datetime.now().hour
        
        if current_hour in self.context_memory:
            hour_data = self.context_memory[current_hour]
            most_common = max(hour_data, key=hour_data.get)
            return f"Based on your usual pattern at this time, you might want to {most_common}."
        
        return None

    def adapt_speech_rate(self):
        """Adapt speech rate based on user interaction patterns"""
        if len(self.command_history) > 10:
            recent_commands = self.command_history[-10:]
            avg_response_time = sum(1 for cmd in recent_commands if "repeat" in cmd.get("command", ""))
            
            if avg_response_time > 3:  
                current_rate = self.engine.getProperty("rate")
                new_rate = max(100, current_rate - 10) 
                self.engine.setProperty("rate", new_rate)
                self.speak("I've slowed down my speech for you.")
            elif avg_response_time == 0:  
                current_rate = self.engine.getProperty("rate")
                new_rate = min(200, current_rate + 5)  
                self.engine.setProperty("rate", new_rate)

    def handle_learn_command(self, command):
        """Handle learning-related commands"""
        if "new command" in command or "custom command" in command:
            self.speak("What would you like to teach me? Say 'when I say' followed by your phrase, then 'do' followed by the action.")
          
            return
        
        elif "preferences" in command:
            self.speak("I can learn your preferences. For example, say 'I prefer fast speech' or 'I prefer detailed responses'")
            return
        
        elif "show what you learned" in command or "what did you learn" in command:
            total_commands = len(self.command_history)
            patterns_learned = len(self.command_patterns)
            self.speak(f"I've learned from {total_commands} commands and recognized {patterns_learned} different action patterns.")
            
          
            if self.command_patterns:
                most_common = max(self.command_patterns.keys(), key=lambda x: len(self.command_patterns[x]))
                self.speak(f"Your most common action is {most_common}.")
            return
        
        elif "forget" in command:
            if "everything" in command:
                self.command_history = []
                self.command_patterns = {}
                self.context_memory = {}
                self.user_preferences = {}
                self.save_learning_data()
                self.speak("I've cleared all my learning data and will start fresh.")
            else:
                self.speak("What would you like me to forget? Say 'forget everything' to clear all data.")
            return
        
        else:
            self.speak("I'm always learning from our interactions. You can say 'show what you learned', 'learn new command', 'learn preferences', or 'forget everything'.")

    def handle_adapt_command(self, command):
        """Handle adaptation-related commands"""
        if "speech" in command or "voice" in command:
            if "faster" in command or "speed up" in command:
                current_rate = self.engine.getProperty("rate")
                new_rate = min(250, current_rate + 20)
                self.engine.setProperty("rate", new_rate)
                self.user_preferences["speech_rate"] = new_rate
                self.speak("I've increased my speech speed.")
                
            elif "slower" in command or "slow down" in command:
                current_rate = self.engine.getProperty("rate")
                new_rate = max(80, current_rate - 20)
                self.engine.setProperty("rate", new_rate)
                self.user_preferences["speech_rate"] = new_rate
                self.speak("I've decreased my speech speed.")
                
            elif "normal" in command or "default" in command:
                self.engine.setProperty("rate", 150)
                self.user_preferences["speech_rate"] = 150
                self.speak("I've set my speech to normal speed.")
            else:
                current_rate = self.engine.getProperty("rate")
                self.speak(f"My current speech rate is {current_rate}. Say 'adapt speech faster', 'slower', or 'normal'.")
                
        elif "response" in command or "answers" in command:
            if "detailed" in command or "more detail" in command:
                self.user_preferences["response_style"] = "detailed"
                self.speak("I'll provide more detailed responses from now on.")
                
            elif "brief" in command or "short" in command:
                self.user_preferences["response_style"] = "brief"
                self.speak("I'll keep my responses brief.")
                
            elif "normal" in command:
                self.user_preferences["response_style"] = "normal"
                self.speak("I'll use normal response style.")
            else:
                current_style = self.user_preferences.get("response_style", "normal")
                self.speak(f"My current response style is {current_style}. Say 'adapt responses detailed', 'brief', or 'normal'.")
                
        elif "sensitivity" in command:
            if "high" in command or "more sensitive" in command:
                self.user_preferences["command_sensitivity"] = "high"
                self.speak("I'll be more sensitive to voice commands and respond to partial matches.")
                
            elif "low" in command or "less sensitive" in command:
                self.user_preferences["command_sensitivity"] = "low"
                self.speak("I'll require more precise commands before responding.")
                
            elif "normal" in command:
                self.user_preferences["command_sensitivity"] = "normal"
                self.speak("I've set command sensitivity to normal.")
            else:
                current_sensitivity = self.user_preferences.get("command_sensitivity", "normal")
                self.speak(f"Current sensitivity is {current_sensitivity}. Say 'adapt sensitivity high', 'low', or 'normal'.")
                
        else:
            self.speak("I can adapt my speech speed, response style, or command sensitivity. Try saying 'adapt speech faster', 'adapt responses detailed', or 'adapt sensitivity high'.")
        
        self.save_learning_data()

    def open_notepad(self):
        try:
            subprocess.Popen("notepad.exe")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error opening Notepad: {e}")
            return False

    def focus_notepad(self, filename=None):
        try:
            import pygetwindow as gw
            if filename:
                notepad_windows = gw.getWindowsWithTitle(filename)
            else:
                notepad_windows = gw.getWindowsWithTitle("Notepad")
            if notepad_windows:
                notepad_windows[0].activate()
                time.sleep(0.5)
                return True
            else:
                return False
        except ImportError:
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.5)
            return True
        return False

    def insert_in_notepad(self, text):
        import re
        match = re.search(r'(insert|write|right)\s+"(.+?)"\s+to\s+(.+)', text)
        if match:
            content = match.group(2).strip()
            filename = match.group(3).strip()
            focused = self.focus_notepad(filename)
            if focused:
                pyautogui.write(content + "\n")
                self.speak(f'I have inserted: {content} to {filename}')
            else:
                self.speak(f'Notepad with filename "{filename}" is not open.')
            return
        # Fallback: old behavior
        for trigger in ["insert ", "write ", "right "]:
            if trigger in text:
                content = text.split(trigger, 1)[1].strip()
                if not self.is_notepad_open():
                    self.open_notepad()
                else:
                    self.focus_notepad()
                pyautogui.write(content + "\n")
                self.speak(f"I have inserted: {content}")
                return
        self.speak('Please tell me what to insert using the command "insert your text" or "insert text to filename"')

    def backspace_notepad(self, filename=None):
        focused = self.focus_notepad(filename)
        if not focused:
            if filename:
                self.speak(f'Notepad with filename "{filename}" is not open.')
            else:
                self.speak('Notepad is not open.')
            return
        pyautogui.hotkey('ctrl', 'backspace')
        self.speak("I have deleted the last word.")

    def clear_notepad(self, filename=None):
        focused = self.focus_notepad(filename)
        if not focused:
            if filename:
                self.speak(f'Notepad with filename "{filename}" is not open.')
            else:
                self.speak('Notepad is not open.')
            return
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('backspace')
        self.speak("I have cleared all text.")

    def read_notes_file(self):
        try:
            with open("notes.txt", "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                self.speak("Here is what you have noted:")
                self.speak(content)
            else:
                self.speak("Your notes file is empty.")
        except FileNotFoundError:
            self.speak("No notes file found.")
        except Exception as e:
            print(f"Error reading notes file: {e}")
            self.speak("I could not read your notes.")

    def close_notepad(self):
        try:
            os.system('taskkill /IM notepad.exe /F')
            self.speak("I have closed Notepad.")
        except Exception as e:
            print(f"Error closing Notepad: {e}")
            self.speak("I could not close Notepad.")

    def is_notepad_open(self):
        try:
            output = subprocess.check_output('tasklist /FI "IMAGENAME eq notepad.exe"', shell=True).decode()
            return "notepad.exe" in output
        except:
            return False

    def run(self):
        running = True
        self.speak("How can I help you today?")
        
        
        suggestion = self.get_contextual_suggestions()
        if suggestion:
            self.speak(suggestion)
        
        while running:
            command = self.listen()
            action_taken = "unknown"
            
            if not command:
                continue
                
          
            predicted_action, confidence = self.predict_intent(command)
            if predicted_action and confidence > 0.8:
                self.speak(f"I think you want to {predicted_action}. Let me do that for you.")
                action_taken = predicted_action
            
            if "exit" in command or "quit" in command or "goodbye" in command:
                action_taken = "exit"
                self.speak("Goodbye! Have a nice day.")
                running = False
                
            elif "note " in command:
                action_taken = "create_note"
                self.insert_in_notepad(command)
            elif any(trigger in command for trigger in ["insert ", "write ", "right "]):
                action_taken = "insert_text"
                self.insert_in_notepad(command)
                
            elif "read" in command:
                action_taken = "read_notes"
                self.read_notes_file()
            elif "close notepad" in command:
                action_taken = "close_notepad"
                self.close_notepad()
                
            elif "backspace" in command or "back word" in command or "delete word" in command:
                action_taken = "backspace"
                import re
                match = re.search(r'(backspace|back word|delete word)\s+in\s+(.+)', command)
                if match:
                    filename = match.group(2).strip()
                    self.backspace_notepad(filename)
                else:
                    self.backspace_notepad()

            elif "clear" in command or "clear all" in command:
                action_taken = "clear_text"
                import re
                match = re.search(r'(clear|clear all)\s+in\s+(.+)', command)
                if match:
                    filename = match.group(2).strip()
                    self.clear_notepad(filename)
                else:
                    self.clear_notepad()
                    
            elif "open notepad" in command:
                action_taken = "open_notepad"
                self.open_notepad()
                self.speak("I have opened Notepad for you.")
                
            elif "hello" in command or "hi" in command:
                action_taken = "greeting"
                self.speak("Hello! I am Pika, your AI voice assistant.")
                
            elif "learn" in command or "remember" in command:
                action_taken = "learning_request"
                self.handle_learn_command(command)
                
            elif "adapt" in command or "adjust" in command:
                action_taken = "adaptation_request"
                self.handle_adapt_command(command)
                
            elif command:
                action_taken = "unknown_command"
             
                similar_commands = []
                for action, patterns in self.command_patterns.items():
                    for pattern in patterns:
                        if SequenceMatcher(None, command, pattern).ratio() > 0.5:
                            similar_commands.append(action)
                
                if similar_commands:
                    suggestion = max(set(similar_commands), key=similar_commands.count)
                    self.speak(f"I'm not sure, but did you mean to {suggestion}? I'm learning from this interaction.")
                else:
                    self.speak("I'm not sure how to help with that, but I'm learning from this interaction. You can ask me to write text, read text, backspace, clear, or open Notepad.")
            
        
            self.learn_from_command(command, action_taken)

def main():
    pika = Pika()
    try:
        pika.run()
    except KeyboardInterrupt:
        print("\nPika voice assistant terminated.")

if __name__ == "__main__":
    main()
