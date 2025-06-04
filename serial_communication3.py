import serial
import time

ESP32_PORT = "COM8"  # ESP32 port
BAUD_RATE = 115200

# Open serial connection once at the start
esp = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Give ESP32 time to initialize

def send_command_to_esp32(command):
    """ Sends a command to ESP32 exactly like the test script. """
    try:
        full_command = f"{command}\n".encode("utf-8")  # Encode command properly
        print(f"Sending command to ESP32: {full_command}")  # Debugging
        esp.write(full_command)  # Send command

        # Read response (if any)
        response = esp.readline().decode("utf-8", errors="ignore").strip()
        if response:
            print(f"ESP32 Response: {response}")

    except Exception as e:
        print(f"Error sending command to ESP32: {e}")

# Keep the connection open so we don’t have to reopen it each time
