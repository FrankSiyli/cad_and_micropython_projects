from machine import Pin, PWM

led = PWM(Pin(25))

# command: led.duty()               // query the default duty
# output: 512

# command: led.freq()               // query the default frequency
# output: 5000

# command: led.duty(100)            // sets the duty to 100

# command: led.freq(1)              // sets the freq to 1 Hertz

# command: led.deinit()              // deinitialise the pwm pin


led = PWM(Pin(25), freq=4, duty=400)  # // all in one command
