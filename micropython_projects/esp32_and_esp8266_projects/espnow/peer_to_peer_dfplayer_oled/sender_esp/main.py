import network
from machine import Pin, I2C, ADC, WDT
import espnow
import utime
import ssd1306
import math

i2c = I2C(0, sda=Pin(4), scl=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

sta = network.WLAN(network.STA_IF)
sta.active(True)

esp = espnow.ESPNow()
esp.active(True)

peer = b"\x08:\x8d\x9a<\x0c"
esp.add_peer(peer)

button_pin = Pin(18, Pin.IN, Pin.PULL_UP)
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)

last_button_state = 1
debounce_delay = 50
display_on_time = 0

wdt = WDT(timeout=30000)


def rotate_line(x1, y1, x2, y2, theta):
    radians = math.radians(theta)
    cos_theta = math.cos(radians)
    sin_theta = math.sin(radians)

    x1_rotated = x1 * cos_theta - y1 * sin_theta + 10
    y1_rotated = x1 * sin_theta + y1 * cos_theta
    x2_rotated = x2 * cos_theta - y2 * sin_theta + 10
    y2_rotated = x2 * sin_theta + y2 * cos_theta

    return x1_rotated, y1_rotated, x2_rotated, y2_rotated


def display_text(text1, text2):
    oled.fill(0)
    oled.text(text1, 10, 30)
    oled.text(text2, 30, 50)
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
    utime.sleep(3)


def draw_logo():
    oled.fill_rect(25, 15, 80, 1, 1)  # top border
    oled.fill_rect(25, 63, 80, 1, 1)  # bottom border
    oled.fill_rect(25, 15, 1, 75, 1)  # left border
    oled.fill_rect(105, 15, 1, 75, 1)  # right border
    oled.fill_rect(29, 19, 38, 4, 1)  # first line
    oled.fill_rect(70, 19, 20, 4, 1)  # second line
    oled.fill_rect(93, 19, 9, 4, 1)  # third line
    oled.text("European", 29, 30)

    # First rotated line X
    x1, y1, x2, y2 = rotate_line(50, 19, 50, 40, 30)
    for offset in range(-2, 2):
        oled.line(int(x1) + offset, int(y1), int(x2) + offset, int(y2), 1)

    # Second rotated line X
    x1, y1, x2, y2 = rotate_line(0, 48, 0, 69, -30)
    for offset in range(-2, 2):
        oled.line(int(x1) + offset, int(y1), int(x2) + offset, int(y2), 1)

    oled.fill_rect(50, 41, 14, 3, 1)  # F
    oled.fill_rect(50, 41, 3, 19, 1)  # F
    oled.fill_rect(50, 48, 10, 3, 1)  # F
    oled.fill_rect(67, 41, 14, 3, 1)  # E
    oled.fill_rect(67, 41, 3, 19, 1)  # E
    oled.fill_rect(67, 48, 13, 3, 1)  # E
    oled.fill_rect(67, 57, 14, 3, 1)  # E
    oled.fill_rect(85, 41, 3, 19, 1)  # L
    oled.fill_rect(85, 57, 14, 3, 1)  # L
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


def update_display(voltage):
    display_text("We are heading", "up to you")
    display_text("Enjoy your day", "    at")
    oled.fill(0)
    draw_logo()
    oled.show()
    utime.sleep(3)


def read_battery_voltage():
    adc_value = adc.read()
    voltage = adc_value * (3.3 / 4095) * 2 + 0.34
    return voltage


while True:
    wdt.feed()
    voltage = read_battery_voltage()

    if display_on_time > 0:
        update_display(voltage)
        display_on_time -= 1
    else:
        oled.fill(0)
        oled.show()

    current_button_state = button_pin.value()

    if current_button_state != last_button_state:
        utime.sleep_ms(debounce_delay)
        current_button_state = button_pin.value()

        if current_button_state != last_button_state:
            if current_button_state == 0:
                message = "makeItHappen"
                try:
                    esp.send(peer, message)
                    print("Message sent:", message)
                    display_on_time = 3
                except Exception as e:
                    print("Error sending message:", e)

            last_button_state = current_button_state
