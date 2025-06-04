from vosk import Model, KaldiRecognizer
import pyaudio
import json
import time

# Load the Vosk speech recognition model
model = Model("vosk-model-small-en-us-0.15")  # Path to Vosk model
recognizer = KaldiRecognizer(model, 16000)

# Initialize PyAudio
p = pyaudio.PyAudio()

def detect_wake_word():
    """ Listens for 'Hey Aura' using Vosk and returns True if detected. """
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Listening for 'Hey Aura'...")

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").lower()
            print(f"Heard: {text}")
            if "hey aura" in text:
                print("Wake word confirmed!")
                stream.stop_stream()
                stream.close()
                return True 

            
def capture_user_response(timeout=10):
    """ Listens for the user's response with an adjustable timeout to capture full input. """
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print(f"Listening for response... Speak now (timeout: {timeout}s).")

    full_text = ""  # Store full response
    start_time = time.time()

    while time.time() - start_time < timeout:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").lower()
            print(f"Heard: {text}")

            if text:
                full_text += " " + text  # Append new words
                start_time = time.time()  # Reset timeout to keep listening

    stream.stop_stream()
    stream.close()

    return full_text.strip()  # Return full response



