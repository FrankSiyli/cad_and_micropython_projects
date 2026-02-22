from machine import Pin
import uasyncio

LED_PIN = 25
BTN_PIN = 27
BLINK_DELAY = 0.5
BUTTON_POLL_DELAY = 0.2

led = Pin(LED_PIN, Pin.OUT)
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)
led_state = False


async def blink(delay):
    global led_state
    while True:
        led_state = not led_state
        led.value(led_state)
        await uasyncio.sleep(delay)


async def wait_button():
    btn_prev = btn.value()
    while True:
        await uasyncio.sleep(BUTTON_POLL_DELAY)
        current_value = btn.value()
        if current_value != btn_prev:
            await uasyncio.sleep(0.02)
            if current_value == btn.value():
                return current_value
        btn_prev = current_value


async def main():
    uasyncio.create_task(blink(BLINK_DELAY))
    while True:
        button_value = await wait_button()
        if button_value == 0:
            print("Button pressed!")


try:
    uasyncio.run(main())
except KeyboardInterrupt:
    pass
