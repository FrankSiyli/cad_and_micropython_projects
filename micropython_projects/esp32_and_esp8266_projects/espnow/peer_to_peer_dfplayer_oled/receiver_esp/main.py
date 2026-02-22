import network
import espnow
import machine
from machine import Pin, I2C, ADC
import utime
from utime import sleep
import json
import ssd1306

i2c = I2C(0, sda=Pin(4), scl=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)

DFPLAYER_UART = machine.UART(1, baudrate=9600, tx=17, rx=16)

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

esp = espnow.ESPNow()
esp.active(True)

max_volume = 30
volume = 10
track_id = 1

button_volume_up = Pin(13, Pin.IN, Pin.PULL_UP)
button_volume_down = Pin(15, Pin.IN, Pin.PULL_UP)
button_next_song = Pin(2, Pin.IN, Pin.PULL_UP)
button_stop_song = Pin(12, Pin.IN, Pin.PULL_UP)

last_volume_up_press = 0
last_volume_down_press = 0
last_next_song_press = 0
last_stop_song_press = 0
debounce_delay = 200

DFPLAYER_BUSY_PIN = 27

dfplayer_busy = Pin(DFPLAYER_BUSY_PIN, Pin.IN)


def dfplayer_busy_handler(pin):
    utime.sleep(0.2)
    if not pin.value():
        pass
    else:
        oled.fill(0)
        oled.show()


def send_command(command, parameter=0):
    query = bytes([0x7E, 0xFF, 0x06, command, 0x00, 0x00, parameter, 0xEF])
    DFPLAYER_UART.write(query)


def update_display(volume, track_id, voltage):
    oled.fill(0)
    oled.text("Volume: {}".format(volume), 30, 30)
    oled.text("Track: {}".format(track_id), 35, 50)
    if voltage >= 3.8:
        oled.fill_rect(105, 0, 25, 10, 1)
        oled.fill_rect(105, 0, 1, 10, 1)
        oled.fill_rect(101, 3, 4, 4, 1)
    elif voltage >= 3.5:
        oled.fill_rect(117, 0, 15, 10, 1)
        oled.fill_rect(105, 0, 25, 1, 1)
        oled.fill_rect(105, 10, 25, 1, 1)
        oled.fill_rect(105, 0, 1, 10, 1)
        oled.fill_rect(101, 3, 4, 4, 1)
    else:
        oled.fill_rect(127, 0, 1, 10, 1)
        oled.fill_rect(105, 0, 25, 1, 1)
        oled.fill_rect(105, 10, 25, 1, 1)
        oled.fill_rect(105, 0, 1, 10, 1)
        oled.fill_rect(101, 3, 4, 4, 1)
    oled.show()


def read_battery_voltage():
    adc.read()
    adc_value = adc.read()
    voltage = adc_value * (3.3 / 4095) * 2 + 0.34
    return voltage


def volume_up(pin):
    global volume, last_volume_up_press
    current_time = utime.ticks_ms()
    if current_time - last_volume_up_press > debounce_delay:
        last_volume_up_press = current_time
        volume = min(volume + 1, max_volume)
        send_command(0x04)
        save_volume(volume)
        update_display(volume, track_id, read_battery_voltage())


def volume_down(pin):
    global volume, last_volume_down_press
    current_time = utime.ticks_ms()
    if current_time - last_volume_down_press > debounce_delay:
        last_volume_down_press = current_time
        volume = max(volume - 1, 0)
        send_command(0x05)
        save_volume(volume)
        update_display(volume, track_id, read_battery_voltage())


def stop_song(pin):
    global last_stop_song_press
    current_time = utime.ticks_ms()
    if current_time - last_stop_song_press > debounce_delay:
        last_stop_song_press = current_time
        send_command(0x16)
        oled.fill(0)
        oled.show()


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
    global last_next_song_press, track_id
    voltage = read_battery_voltage()
    current_time = utime.ticks_ms()
    if current_time - last_next_song_press > debounce_delay:
        last_next_song_press = current_time
        track_id = track_id + 1 if track_id < 10 else 1
        save_track_id(track_id)
        update_display(volume, track_id, voltage)
        send_command(0x03, track_id)


def save_track_id(track_id):
    try:
        with open("track_id.json", "w") as f:
            json.dump({"track_id": track_id}, f)
    except Exception as e:
        pass


def load_track_id():
    try:
        with open("track_id.json", "r") as f:
            data = json.load(f)
            track_id = data.get("track_id", 1)
            if isinstance(track_id, int):
                return track_id
            else:
                return 1
    except Exception as e:
        return 1


def main():
    global volume, track_id
    volume = load_volume()
    track_id = load_track_id()
    voltage = read_battery_voltage()
    utime.sleep(0.1)
    send_command(0x06, volume)
    utime.sleep(0.1)
    update_display(volume, track_id, voltage)
    send_command(0x03, track_id)
    send_command(0x16)

    while True:
        _, msg = esp.recv()
        if msg:
            if msg == b"makeItHappen":
                print("Message received:", msg)
                machine.reset()
                return
            else:
                print("Unknown message!")


# Initialize pins and interrupts
button_volume_up.irq(trigger=Pin.IRQ_FALLING, handler=volume_up)
button_volume_down.irq(trigger=Pin.IRQ_FALLING, handler=volume_down)
button_next_song.irq(trigger=Pin.IRQ_FALLING, handler=next_song)
button_stop_song.irq(trigger=Pin.IRQ_FALLING, handler=stop_song)
dfplayer_busy.irq(
    trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=dfplayer_busy_handler
)

main()


if __name__ == "__main__":
    main()
