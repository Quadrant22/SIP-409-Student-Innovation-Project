import pygame
import random
import time
import pyttsx3

# Initialize Pygame mixer
pygame.mixer.init()

# Initialize TTS Engine
engine = pyttsx3.init()
engine.setProperty('rate', 210)  
engine.setProperty('volume', 1.0)


# Load sound effects
background_sound = "sounds/birds_low_volume.mp3"  
wake_sound = pygame.mixer.Sound("sounds/Glitter Sound.mp3")
shutdown_fade = pygame.mixer.Sound("sounds/EndingsMusicPlay.mp3")
explanation_music = "sounds/ExplanationMusic.mp3"  
lights_music = "sounds/LightsOn.mp3"  


# AuraSync Introduction
aura_sync_intro = (
    "You are a being of light. When challenges arise, parts of your light may dim, seeking renewal. "
    "Through meditation or within an illuminated space, you can restore balance and bring light back to those parts of yourself. "
    "Let the glow surround you, uplift you, and guide you forward. "
    "Welcome to AuraSync!"
)

# Randomized activation phrases
activation_phrases = [
    "I now call upon the celestial radiance to embrace this beautiful soul. Lights, awaken.",
    "Cosmic light, shine upon this being. Illuminate, uplift, and bless. Lights, activate.",
    "With gratitude, I welcome the heavens glow. May this radiance uplift you. Activate lights.",
    "Stars above, share your sacred brilliance. Let your light dance upon this soul. Lights, awaken.",
    "In kindness and grace, may this cosmic energy flow. Shine, illuminate, and bless. Lights, activate."
]

# Wisdom Phrases
wisdom_phrases = [
    "The universe breathes with you...",
    "The unseen is near...",
    "Listen to your heart...",
    "Let go of your troubles...",
    "Dear Universe, Light me up, set me free, to be all that I can be..."
]

# Randomized shutdown phrases
shutdown_phrases = [
    "Your light now shines beyond the stars. Go forth, radiant and free. Until we meet again.",
    "The universe watches over you. Let the cosmic glow guide your path. Farewell, seeker of light.",
    "The stars whisper your name into infinity. Rest now in their glow, until the light calls again.",
    "The energy of the cosmos is now within you. Carry it with grace. Until next time.",
    "Every end is a new beginning. The universe awaits your return. Be well, celestial traveler."
]
def play_background_sound(volume=0.01):
    """ Play a looping ambient background sound during idle mode. """
    pygame.mixer.music.load(background_sound)
    pygame.mixer.music.play(-1)  # Loop indefinitely
    print("Background sound started.")

def stop_background_sound():
    """ Stop the background sound when wake word is detected. """
    pygame.mixer.music.stop()
    print("Background sound stopped.")

def speak_wisdom_phrases():
    """ Selects and speaks three different wisdom phrases with pauses in between. """
    chosen_phrases = random.sample(wisdom_phrases, 3)  # Pick 3 unique phrases

    for phrase in chosen_phrases:
        print(f"Speaking: {phrase}")
        engine.say(phrase)
        engine.runAndWait()
        time.sleep(5)  # Pause before the next phrase


def play_wake_sound():
    """ Plays a soft chime when wake word is detected. """
    wake_sound.play()


def play_explanation_music():
    """ Plays background music while the AI explains a flame or purpose. """
    pygame.mixer.music.load(explanation_music)
    pygame.mixer.music.play(-1)  # Loop until explanation ends

def stop_explanation_music():
    """ Stops explanation background music after AI finishes speaking. """
    pygame.mixer.music.stop()

def fade_out_explanation_music(fade_time=4):
    """ Fades out the explanation music smoothly before activation. """
    if pygame.mixer.music.get_busy():  # Check if music is playing
        pygame.mixer.music.fadeout(fade_time * 1000)  # Convert seconds to milliseconds
        time.sleep(fade_time)  # Allow fadeout to complete before moving on

def play_lights_music():
    """ Plays the special music when lights activate, without restarting if already playing. """
    if not pygame.mixer.music.get_busy():  # Check if music is already playing
        pygame.mixer.music.load(lights_music)
        pygame.mixer.music.play(-1)  # Loop until manually stopped
    else:
        print("Lights music is already playing, no need to restart.")

def fade_out_lights_music(fade_time=4):
    """ Fades out the lights activation music smoothly before stopping. """
    if pygame.mixer.music.get_busy():  # Check if music is playing
        pygame.mixer.music.fadeout(fade_time * 1000)  # Convert seconds to milliseconds
        time.sleep(fade_time)  # Allow fadeout to complete before moving on
        print("Lights music faded out.")


def get_activation_phrase():
    """ Returns a random activation phrase. """
    return random.choice(activation_phrases)


def play_activation_music():
    """ Plays instrumental music while lights are active, then stops. """
    pygame.mixer.music.stop()  # Stop previous sounds
    pygame.mixer.music.load(lights_music)
    pygame.mixer.music.play()
    time.sleep(50)  # Ensures the music plays for 50 seconds
    pygame.mixer.music.stop()  # Stops music after 50 seconds


def play_shutdown():
    """ Starts shutdown music immediately while AI speaks its final words. """
    pygame.mixer.music.stop()  # Stops existing music
    pygame.mixer.music.load("sounds/EndingsMusicPlay.mp3")  # Load shutdown music
    pygame.mixer.music.play()  # Start playing immediately

    return random.choice(shutdown_phrases)  # AI speaks while music plays

def fade_out_shutdown_music(fade_time=4):
    """ Fades out the shutdown music smoothly before stopping. """
    if pygame.mixer.music.get_busy():  # Check if music is playing
        pygame.mixer.music.fadeout(fade_time * 1000)  # Convert seconds to milliseconds
        time.sleep(fade_time)  # Allow fadeout to complete before moving on
        print("Shutdown music faded out.")

