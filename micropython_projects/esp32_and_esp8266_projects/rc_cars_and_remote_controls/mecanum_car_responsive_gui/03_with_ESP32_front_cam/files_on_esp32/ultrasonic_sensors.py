from machine import Pin
from machine import time_pulse_us
import time

TRIG_PIN_FRONT = 15
ECHO_PIN_FRONT = 13

TRIG_PIN_REAR = 0
ECHO_PIN_REAR = 2

trig_pin_front = Pin(TRIG_PIN_FRONT, Pin.OUT)
echo_pin_front = Pin(ECHO_PIN_FRONT, Pin.IN)

trig_pin_rear = Pin(TRIG_PIN_REAR, Pin.OUT)
echo_pin_rear = Pin(ECHO_PIN_REAR, Pin.IN)

def get_distance_front():
    trig_pin_front.value(0)
    time.sleep_us(5)
    trig_pin_front.value(1)
    time.sleep_us(10)
    trig_pin_front.value(0)
    duration = time_pulse_us(echo_pin_front, 1)
    distance_front = duration / 58
    return int(distance_front)

def get_distance_rear():
    trig_pin_rear.value(0)
    time.sleep_us(5)
    trig_pin_rear.value(1)
    time.sleep_us(10)
    trig_pin_rear.value(0)
    duration = time_pulse_us(echo_pin_rear, 1)
    distance_rear = duration / 58
    return int(distance_rear)
