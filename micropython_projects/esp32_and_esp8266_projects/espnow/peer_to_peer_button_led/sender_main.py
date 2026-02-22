import network
from machine import Pin
import espnow
import utime


# WLAN interface must be active to send/recv
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()  # For ESP8266

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

# Define the MAC address of the receiving ESP32 (ESP32 B)
peer = b"\x08:\x8d\x9aH0"
esp.add_peer(peer)

# Create a function to send data when a button is pressed
button_pin = Pin(18, Pin.IN, Pin.PULL_UP)

# Initialize variables for debouncing
last_button_state = 1  # Assuming the button is not pressed initially
debounce_delay = 50  # Adjust value to your needs

while True:
    # Read the button state
    current_button_state = button_pin.value()

    # Check if button state changed
    if current_button_state != last_button_state:
        # Wait to debounce the button
        utime.sleep_ms(debounce_delay)

        # Read the button state again to make sure it's stable
        current_button_state = button_pin.value()

        # If the button state is still different, it's a valid press
        if current_button_state != last_button_state:
            if current_button_state == 0:
                message = "ledOn"
                print(f"Sending command : {message}")
                esp.send(peer, message)
            else:
                message = "ledOff"
                print(f"Sending command : {message}")
                esp.send(peer, message)

        # Update the last button state
        last_button_state = current_button_state


# my ESPs:
# sender    08:3A:8D:9A:41:D0 b'\x08:\x8d\x9aA\xd0'
# receiver  08:3A:8D:9A:48:30 b'\x08:\x8d\x9aH0'
