import network
import machine
import espnow
import utime
from machine import Pin


# WLAN interface must be active to send/recv
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()  # For ESP8266

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

# Define the MAC address of the receiving ESP32 (ESP32 B)
peer = b'\xc8\xc9\xa3\x10\xcc)'
esp.add_peer(peer)

# Configure button pins
button_pins = [12, 14, 26, 27, 15, 13]
buttons = [machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for pin in button_pins]

# Mapping button pins to commands
button_commands = {
    12: b"forward",
    26: b"reverse",
    14: b"left",
    27: b"right",
    15: b"spinLeft",
    13: b"spinRight"
}

# Initialize variables for debouncing and tracking button press duration
last_button_states = [1] * len(button_pins)  # Assuming all buttons are not pressed initially
debounce_delay = 10  # Adjust value to your needs
press_start_time = [0] * len(button_pins)  # Tracks the time when each button was pressed
stop_delay = 10  # Adjust value to your needs (in milliseconds)

while True:
    for index, button_pin in enumerate(buttons):
        # Read the button state
        current_button_state = button_pin.value()

        # Check if button state changed
        if current_button_state != last_button_states[index]:
            # Wait to debounce the button
            utime.sleep_ms(debounce_delay)

            # Read the button state again to make sure it's stable
            current_button_state = button_pin.value()

            # If the button state is still different, it's a valid press
            if current_button_state != last_button_states[index]:
                if current_button_state == 0:
                    # Button pressed
                    press_start_time[index] = utime.ticks_ms()  # Start measuring press duration
                    command = button_commands.get(button_pins[index])
                    if command:
                        print(f"Sending command: {command}")
                        esp.send(peer, command)
                else:
                    # Button released
                    press_duration = utime.ticks_ms() - press_start_time[index]  # Calculate press duration
                    if press_duration >= stop_delay:
                        # Send stop command if press duration exceeds stop delay
                        print("Sending stop command")
                        esp.send(peer, b"stop")

            # Update the last button state
            last_button_states[index] = current_button_state

