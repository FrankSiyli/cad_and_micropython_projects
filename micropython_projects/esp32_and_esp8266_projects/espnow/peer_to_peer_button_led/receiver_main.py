import network
import espnow
import machine

# A WLAN interface must be active to send/recv
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()  # For ESP8266

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

led_pin = machine.Pin(18, machine.Pin.OUT)

while True:
    _, msg = esp.recv()
    if msg:  # msg == None if timeout in recv()
        if msg == b"ledOn":
            print("Turning on LED")
            led_pin.on()
        elif msg == b"ledOff":
            print("Turning off LED")
            led_pin.off()
        else:
            print("Unknown message!")


# my ESPs:
# sender    08:3A:8D:9A:41:D0 b'\x08:\x8d\x9aA\xd0'
# receiver  08:3A:8D:9A:48:30 b'\x08:\x8d\x9aH0'
