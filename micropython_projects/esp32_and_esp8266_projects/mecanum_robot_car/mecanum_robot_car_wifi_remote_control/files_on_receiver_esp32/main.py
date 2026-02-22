from robot_car import RobotCar
import network
import espnow
from machine import Pin
import time
import threading

# A WLAN interface must be active to send/recv
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()  # For ESP8266

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

# Wifi Robot Car Configuration
MAX_POWER_LEVEL = 65535        # 100%
MEDIUM_POWER_LEVEL = 49151     # 75%
MIN_POWER_LEVEL = 32767        # 50%

front_enable_pins = [23, 22]
front_motor_pins = [19, 21, 25, 33]

rear_enable_pins = [26, 27]
rear_motor_pins = [16, 17, 12, 14]

robot_car = RobotCar(front_enable_pins, rear_enable_pins, front_motor_pins, rear_motor_pins, MAX_POWER_LEVEL)

# Mapping received car commands to robot_car methods
car_commands = {
    b"forward": robot_car.forward,
    b"reverse": robot_car.reverse,
    b"left": robot_car.left,
    b"right": robot_car.right,
    b"spinLeft": robot_car.spinLeft,
    b"spinRight": robot_car.spinRight,
    b"stop": robot_car.stop
}

# Define LED pin and set it as output
led = Pin(13, Pin.OUT)

# Define a function for blinking the LED
def blink_led():
    while True:
        led.value(1)
        time.sleep(0.2) 
        led.value(0)
        time.sleep(0.2)
        led.value(1)
        time.sleep(0.2)
        led.value(0)
        time.sleep(0.5)
        led.value(1)
        time.sleep(0.2)
        led.value(0)
        time.sleep(0.2)
        led.value(1)
        time.sleep(0.2)
        led.value(0)
        time.sleep(0.5)
        led.value(1)
        time.sleep(0.8)
        led.value(0)
        time.sleep(2)

# Start the LED blinking thread
blink_thread = threading.Thread(target=blink_led)
blink_thread.daemon = True  # Daemonize the thread so it exits when the main program exits
blink_thread.start()

while True:
    _, msg = esp.recv()
    if msg:  # msg == None if timeout in recv()
        if msg in car_commands:
            car_commands[msg]()
        else:
            print("Unknown message!")
