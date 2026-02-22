import time
from machine import Pin


def blink_led():
    counter = 10
    p = Pin(25, Pin.OUT)

    while counter > 0:
        p.on()
        time.sleep(1)
        p.off()
        time.sleep(1)
        counter -= 1

    print("Done")
