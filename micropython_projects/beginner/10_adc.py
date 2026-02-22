# KY-018 light sensor connected to +, - and signal to pin 26 on a Lolin32


from machine import ADC, Pin

sensor = ADC(Pin(26))

# command: sensor.read()
# output: current signal e.g.: 2384
