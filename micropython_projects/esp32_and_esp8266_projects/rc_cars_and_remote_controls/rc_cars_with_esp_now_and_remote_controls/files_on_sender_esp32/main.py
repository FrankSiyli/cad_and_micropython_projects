import network
import machine
import espnow
import utime
import esp32
from machine import Pin

# ------------------------------
# WLAN / ESP-NOW Setup
# ------------------------------
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()  # Sicherheitshalber

esp = espnow.ESPNow()
esp.active(True)

# MAC-Adresse des empfangenden ESP32 (ESP32 B)
peer = b'|\x87\xce(\x11X'
esp.add_peer(peer)

# ------------------------------
# Button Setup
# ------------------------------
button_pins = [12, 14, 26, 27, 15, 13]
buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in button_pins]

# Mapping Button -> Command
button_commands = {
    12: b"forward",
    26: b"reverse",
    14: b"left",
    27: b"right",
    15: b"spinLeft",
    13: b"spinRight"
}

# ------------------------------
# Status LED Setup
# ------------------------------
led = Pin(23, Pin.OUT)
led_blink_delay = 500  # ms

# ------------------------------
# Debounce / Timer Setup
# ------------------------------
last_button_states = [1] * len(button_pins)  # Alle Buttons initial HIGH
debounce_delay = 10  # ms
press_start_time = [0] * len(button_pins)
stop_delay = 10  # ms

# Deep Sleep Timer
last_activity = utime.ticks_ms()
sleep_timeout = 10000  # 10 Sekunden

# ------------------------------
# Hauptloop
# ------------------------------
while True:
    now = utime.ticks_ms()

    # LED blinken
    if now % (2 * led_blink_delay) < led_blink_delay:
        led.value(1)
    else:
        led.value(0)

    # Buttons prüfen
    for index, button_pin in enumerate(buttons):
        current_button_state = button_pin.value()

        if current_button_state != last_button_states[index]:
            # Debounce
            utime.sleep_ms(debounce_delay)
            current_button_state = button_pin.value()

            if current_button_state != last_button_states[index]:
                # Activity Reset
                last_activity = now

                if current_button_state == 0:
                    # Button gedrückt
                    press_start_time[index] = utime.ticks_ms()
                    command = button_commands.get(button_pins[index])
                    if command:
                        print(f"Sending command: {command}")
                        esp.send(peer, command)
                else:
                    # Button losgelassen
                    press_duration = utime.ticks_ms() - press_start_time[index]
                    if press_duration >= stop_delay:
                        print("Sending stop command")
                        esp.send(peer, b"stop")

                last_button_states[index] = current_button_state

    # Prüfen, ob Deep Sleep fällig ist
    if utime.ticks_diff(now, last_activity) > sleep_timeout:
        print("Going to deep sleep...")

        # Stabiler Wakeup über Master-Taster (GPIO12)
        esp32.wake_on_ext0(pin=Pin(12, Pin.IN, Pin.PULL_UP), level=0)

        # Board schlafen legen
        machine.deepsleep()
