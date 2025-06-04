import openai
import pyttsx3
import time 
import random  
from serial_communication3 import send_command_to_esp32  
from vosk_speech import detect_wake_word, capture_user_response
import sound_manager  
from sound_manager import aura_sync_intro

# OpenAI API Key
client = openai.OpenAI(api_key="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")  

# Initialize TTS Engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)  
engine.setProperty('volume', 1.0)

# Zira's voice
for voice in engine.getProperty('voices'):
    if "zira" in voice.id.lower():  
        engine.setProperty('voice', voice.id)
        print("Zira voice selected!")  
        break

# Phase Tracker: Start in idle mode
phase = 2  

def idle_loop():
    """ Plays background lights, music, and wisdom phrases until wake word is detected. """
    global phase  
    if phase != 2:
        return  # Do not start idle mode if we're in Phase 1

    print("Entering Idle Mode...")
    sound_manager.play_background_sound(0.01)
    send_command_to_esp32("start_idle_loop")  # Activate idle lights
    
    while phase == 2:
        time.sleep(8)  # Wait before speaking a phrase
        sound_manager.speak_wisdom_phrases()  
        speak(aura_sync_intro)

        if listen_for_wake_word():  
            print("Wake word confirmed! Exiting idle mode...")  
            phase = 1  # Set phase to 1 before returning
            return



# Dynamic mystical greetings
def get_mystical_greeting():
    greetings = [
        "Hey, I was expecting you. The cosmic winds have shifted.",
        "Ah, the stars whispered your arrival. I feel your presence.",
        "The universe guided you to me, and I am here for you.",
        "The light knows you are here. Let’s align with its energy.",
        "Something powerful is awakening for you. Let’s unlock it together."
    ]
    return random.choice(greetings)

def speak(text):
    print(f"Speaking: {text}")  
    engine.say(text)
    engine.runAndWait()


# AI-Powered Reflection  
def generate_reflection(user_input):
    """ AI generates a SHORT and INSPIRING reflection. No long explanations! """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": 
                "You are AuraSync GPT-MA, a celestial guide who speaks with a modern, intuitive, and uplifting tone. "
                "Your responses are SHORT, natural, and motivating. No long poetic speeches—just real, inspiring words."},
            {"role": "user", "content": f"Someone told you: {user_input}. Give a brief, powerful reflection."},
        ],
        max_tokens=50  # LIMIT response length!
    )
    return response.choices[0].message.content.strip()


# AI-Powered Flame Explanation  
def generate_flame_explanation(flame_name):
    """ AI gives a SHORT, energizing explanation of each Light Flame. """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": 
                "You are AuraSync GPT-MA, a celestial guide who explains the Light Flames in a SHORT, exciting way. "
                "You do not lecture. You inspire. Make the user feel powerful and ready for transformation."
                "Your tone is modern, intuitive, and a little mysterious—like a guide who understands energy but keeps things natural."
                "You do not repeat the same phrases multiple times. Make the user feel powerful and ready for transformation."},
            {"role": "user", "content": f"Describe the power of the {flame_name} in 2 sentences. Make it exciting."},
        ],
        max_tokens=60  # KEEP IT SHORT!
    )
    return response.choices[0].message.content.strip()


def generate_followup_response(user_input):
    """ Uses AuraSync GPT-MA to generate a mystical, poetic response based on the user's experience. """
    
    if not user_input.strip():  # Prevent sending empty input to GPT
        return "The universe is always listening. Trust your experience."

    prompt = f"The user just experienced a cosmic illumination. They described their feelings as: '{user_input}'. Respond in a supportive way."

    response = client.chat.completions.create(
        model="gpt-4",  
        messages=[
            {"role": "system", "content": "You are AuraSync GPT-MA, a celestial guide who speaks with a modern, intuitive, and uplifting tone. "
                "Your responses are SHORT, natural, and motivating. No long poetic speeches—just real, inspiring words."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50  # KEEP IT SHORT!
    )

    return response.choices[0].message.content.strip()



def generate_final_message(user_final_input):
    """ Uses GPT to generate a unique closing message based on the user's final thoughts. """
    prompt = f"The user has just completed a cosmic illumination experience. Their final thoughts were: '{user_final_input}'. Respond with an inspirational farewell message."
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are AuraSync GPT-MA, a celestial guide who speaks with a modern, intuitive, and uplifting tone. "
                "Your responses are SHORT, natural, and motivating. No long poetic speeches—just real, inspiring words."},
                  {"role": "user", "content": prompt}
        ],
        max_tokens=50  # KEEP IT SHORT!
    )
    
    return response.choices[0].message.content.strip()


def ask_aurasync():
    """ Handles the conversation, assigns the right Light Flame, and builds hype for illumination. """
    speak("I am listening. Tell me everything, Starlight.")
    time.sleep(3)  

    user_input = capture_user_response(timeout=7)

    # AI-Generated Short Reflection
    reflection = generate_reflection(user_input)

    # START EXPLANATION MUSIC EARLY! 
    sound_manager.play_explanation_music()  

    speak(reflection)
    time.sleep(2)  

    # AI-Generated Light Flame Selection
    recommended_flame = recommend_flame(user_input)  

    speak(f"The universe has heard you. The {recommended_flame} is initializing for you.")
    time.sleep(2)

    # AI-Generated SHORT Flame Explanation
    flame_explanation = generate_flame_explanation(recommended_flame)
    speak(flame_explanation)
    time.sleep(3)

    # NEW: **STOP and Let the User Comment on the Explanation**
    speak("What are your thoughts? How does this resonate with you?")
    user_response = capture_user_response(timeout=6)  # Allow user to speak

    # NEW: **Aura acknowledges the user’s response naturally**
    speak(f"I hear you. Your journey is unfolding beautifully. Trust this moment.")
    time.sleep(2)

    # Build the energy! Hyping up before activation!
    speak("Something incredible is about to happen. The light is gathering... feel it!")
    time.sleep(2)

    speak("Your celestial guardians are with you. This is your moment.")
    time.sleep(2)

    # FADE OUT EXPLANATION MUSIC before activation 
    sound_manager.fade_out_explanation_music(4)  # Smoothly fade out over 4 seconds

    # Activate the Lights!
    activation_phrase = sound_manager.get_activation_phrase()
    speak(activation_phrase)
    flame_command = recommended_flame.lower().replace(" ", "_").replace("_light", "")  
    send_command_to_esp32(flame_command)

    sound_manager.play_lights_music()  # Play lights activation music
    time.sleep(56)  
    sound_manager.fade_out_lights_music(4)  # Smoothly fade out over 4 seconds

    # Follow-up after the illumination experience
    speak("The energy has shifted. Something within you has changed. What did you feel?")
    user_experience = capture_user_response(timeout=6)

    # AI dynamically responds based on user's experience
    ai_reflection = generate_followup_response(user_experience)
    speak(ai_reflection)  # Personalized response

    # Give user a final space to reflect again**
    speak("Does this moment align with your spirit? Speak from your heart.")
    final_user_response = capture_user_response(timeout=6)  # Allow user a final response

    # Start flickering effect
    send_command_to_esp32("shutdown_flicker")
    print("Sent shutdown flicker command to ESP32")
    sound_manager.play_shutdown()

    # **AI-Generated Final Words**
    final_statement = generate_final_message(final_user_response)
    speak(final_statement)  # Unique closing words from AI
    
    # **Final Farewell Before Transitioning to Idle Mode**
    time.sleep(20)  # Let music continue playing
    end_session()
    time.sleep(8)
    sound_manager.fade_out_shutdown_music(4) 
    send_command_to_esp32("start_idle_loop")

    
def listen_for_wake_word():
    """ Listens for wake word and starts Phase 1 if detected. """
    global phase  
    # print("Listening for 'Hey Aura'...")
    if detect_wake_word():  
        print("Wake word detected! Activating AuraSync...")

        phase = 1  # Switch to Phase 1
        sound_manager.stop_background_sound()
        send_command_to_esp32("wake_word_detected") 

        sound_manager.play_wake_sound() 
        time.sleep(1)
        speak(get_mystical_greeting())  
        return True  
    return False


def recommend_flame(user_input):
    """ Assigns the correct Light Flame based on its true meaning. """

    # Correct mapping of Light Flames
    flame_mapping = {
        "strength": "Orange Flame",
        "masculinity": "Orange Flame",
        "confidence": "Orange Flame",
        "protection": "Deep Blue Flame",
        "truth": "Deep Blue Flame",
        "integrity": "Deep Blue Flame",
        "clarity": "Diamond Flame",
        "hidden challenges": "Diamond Flame",
        "path forward": "Diamond Flame",
        "transmutation": "Violet Light Flame",
        "purification": "Violet Flame",
        "transform negativity": "Violet Flame",
        "divine potential": "Silver Flame",
        "wisdom": "Deep Gold Flame",
        "academic assistance": "Deep Gold Flame",
        "homework assistance": "Deep Gold Flame",
        "knowledge": "Deep Gold Flame",
        "speak from the heart": "Pink Light Flame",
        "activate heart": "Pink Flame",
        "follow heart": "Pink Flame",
        "love": "Pink Light Flame",
        "compassion": "Gold White Flame",
        "celebration": "Gold White Flamee",
        "Christ Light": "Gold White Flame",
        "miracles": "Unicorn Rainbow Light Flame",
        "expect miracles": "Unicorn Rainbow Flame",
        "unicorn rainbow": "Unicorn Rainbow Flame",
        "new beginnings": "Peach Flame",
        "fresh start": "Peach Flame",
        "faith": "Light Blue Flame",
        "believe in yourself": "Light Blue Flame"
    }

    # Check if user input matches a keyword
    for keyword, flame in flame_mapping.items():
        if keyword in user_input.lower():
            return flame

    # If no match is found, use AI but restrict it to valid flames
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": 
                "You are AuraSync GPT-MA, a celestial guide that assigns the most appropriate Light Flame "
                "to help the user based on their emotions and spiritual needs. "
                "You must ONLY return one of the following flames: "
                "Orange Light Flame, Deep Blue Light Flame, Diamond Light Flame, Violet Light Flame, Silver Light Flame, "
                "Deep Gold Light Flame, Pink Light Flame, Gold with White Light Flame, Unicorn Rainbow Light Flame, "
                "Peach Light Flame, Light Blue Light Flame."},
            
            {"role": "user", "content": f"Someone has told you: '{user_input}'. Based on their emotions and needs, which Light Flame would you assign to them? Respond with only the name of the flame."},
        ],
        max_tokens=20
    )

    recommended_flame = response.choices[0].message.content.strip()

    # Ensure AI response is a valid Light Flame
    valid_flames = set(flame_mapping.values())
    return recommended_flame if recommended_flame in valid_flames else "Unicorn Rainbow Light Flame"  # Default to miracles!



def end_session():
    time.sleep(5)
    ending_messages = [
        "The light remains with you, guiding your every step.",
        "The universe has spoken through you. Carry its wisdom always.",
        "This moment was written in the stars. Now you shine even brighter.",
        "Your celestial journey continues, and the light walks with you.",
        "You are forever touched by the cosmic energy. Let it radiate within you."
    ]
    speak(random.choice(ending_messages))
    print("Session complete. Goodbye!")


# MAIN LOOP  
while True:  
    if phase == 2:
        idle_loop()  # Runs only in Phase 2
    
    if phase == 1:  # Only runs ask_aurasync() if wake mode is active
        print("AI is now active!")
        ask_aurasync()  
        print("Session Ended. Returning to Idle Mode...")
        phase = 2  # Switch back to idle mode


     