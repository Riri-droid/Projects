pip install -r requirements.txt# Pika - Your Voice Assistant

A simple voice assistant that can recognize speech, transcribe to a text editor, and read text aloud.

## Features

- Voice recognition (Speech-to-Text)
- Text-to-Speech capability
- Notepad integration for transcribing and reading text

## Requirements

- Python 3.6+
- Required libraries (install with pip):
  - speech_recognition
  - pyttsx3
  - pyautogui

## Installation

```bash
pip install SpeechRecognition pyttsx3 pyautogui
```

## Usage

Run the main script:

```bash
python src/pika.py
```

## Commands

- "Write [your text]" - Writes the specified text to Notepad
- "Read" - Reads the text currently in Notepad
- "Clear" - clears the full notepad
- "Backspace" - clears the last word in the notepad
- "Exit" - Exits the program

