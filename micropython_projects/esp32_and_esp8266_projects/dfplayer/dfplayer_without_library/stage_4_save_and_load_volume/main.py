import machine
from machine import Pin
import utime
from utime import sleep
import json


DFPLAYER_UART = machine.UART(1, baudrate=9600, tx=17, rx=16)

max_volume = 30
volume = 0

button_volume_up = Pin(13, Pin.IN, Pin.PULL_UP)
button_volume_down = Pin(15, Pin.IN, Pin.PULL_UP)
button_next_song = Pin(2, Pin.IN, Pin.PULL_UP)

last_volume_up_press = 0
last_volume_down_press = 0
last_next_song_press = 0
debounce_delay = 200


def send_command(command, parameter=0):
    query = bytes([0x7E, 0xFF, 0x06, command, 0x00, 0x00, parameter, 0xEF])
    DFPLAYER_UART.write(query)
    utime.sleep(0.1)


def volume_up(pin):
    global volume, last_volume_up_press
    current_time = utime.ticks_ms()
    if current_time - last_volume_up_press > debounce_delay:
        last_volume_up_press = current_time
        volume = min(volume + 1, max_volume)
        send_command(0x04)
        save_volume(volume)


def volume_down(pin):
    global volume, last_volume_down_press
    current_time = utime.ticks_ms()
    if current_time - last_volume_down_press > debounce_delay:
        last_volume_down_press = current_time
        volume = max(volume - 1, 0)
        send_command(0x05)
        save_volume(volume)


def save_volume(volume):
    try:
        with open("volume.json", "w") as f:
            json.dump({"volume": volume}, f)
    except Exception as e:
        pass


def load_volume():
    try:
        with open("volume.json", "r") as f:
            data = json.load(f)
            volume = data.get("volume", 15)
            if isinstance(volume, int):
                return volume
            else:
                return 15
    except Exception as e:
        return 15


def next_song(pin):
    global last_next_song_press
    current_time = utime.ticks_ms()
    if current_time - last_next_song_press > debounce_delay:
        last_next_song_press = current_time
        send_command(0x01)


def main():
    global volume
    volume = load_volume()  # load last volume status
    send_command(0x06, volume)  # set volume
    utime.sleep(0.3)
    send_command(0x0D)  # start playback
    # Wait for the song to finish playing
    while True:
        is_playing_response = is_playing()
        if not is_playing_response:
            # Song has finished playing, send stop command
            send_command(0x16)
            break
        utime.sleep(1)


# Initialize pins and interrupts
button_volume_up.irq(trigger=Pin.IRQ_FALLING, handler=volume_up)
button_volume_down.irq(trigger=Pin.IRQ_FALLING, handler=volume_down)
button_next_song.irq(trigger=Pin.IRQ_FALLING, handler=next_song)

if __name__ == "__main__":
    main()
