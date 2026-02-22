from machine import Pin, PWM



class RobotCar:
    def __init__(
        self,
        front_enable_pins,
        front_motor_pins,
        speed,
    ):
        self.front_right_motor_enable_pin = PWM(Pin(front_enable_pins[0]), freq=2000)
        self.front_left_motor_enable_pin = PWM(Pin(front_enable_pins[1]), freq=2000)
        
        self.front_right_motor_control_1 = Pin(front_motor_pins[0], Pin.OUT)
        self.front_right_motor_control_2 = Pin(front_motor_pins[1], Pin.OUT)
        self.front_left_motor_control_1 = Pin(front_motor_pins[2], Pin.OUT)
        self.front_left_motor_control_2 = Pin(front_motor_pins[3], Pin.OUT)

        
        self.speed = speed

    def stop(self):
        self.front_right_motor_control_1.value(0)
        self.front_right_motor_control_2.value(0)
        self.front_left_motor_control_1.value(0)
        self.front_left_motor_control_2.value(0)
       
        self.front_right_motor_enable_pin.duty_u16(0)
        self.front_left_motor_enable_pin.duty_u16(0)
        
    def forward(self):
        self.front_right_motor_enable_pin.duty_u16(self.speed)
        self.front_left_motor_enable_pin.duty_u16(self.speed)
       
        self.front_right_motor_control_1.value(1)
        self.front_right_motor_control_2.value(0)
        self.front_left_motor_control_1.value(1)
        self.front_left_motor_control_2.value(0)
       
    def reverse(self):
        self.front_right_motor_enable_pin.duty_u16(self.speed)
        self.front_left_motor_enable_pin.duty_u16(self.speed)
       
        self.front_right_motor_control_1.value(0)
        self.front_right_motor_control_2.value(1)
        self.front_left_motor_control_1.value(0)
        self.front_left_motor_control_2.value(1)
        
    def spinRight(self):
        self.front_right_motor_enable_pin.duty_u16(self.speed)
        self.front_left_motor_enable_pin.duty_u16(self.speed)
       
        self.front_right_motor_control_1.value(0)
        self.front_right_motor_control_2.value(1)
        self.front_left_motor_control_1.value(1)
        self.front_left_motor_control_2.value(0)
       
    def spinLeft(self):
        self.front_right_motor_enable_pin.duty_u16(self.speed)
        self.front_left_motor_enable_pin.duty_u16(self.speed)
        
        self.front_right_motor_control_1.value(1)
        self.front_right_motor_control_2.value(0)
        self.front_left_motor_control_1.value(0)
        self.front_left_motor_control_2.value(1)
       
    def right(self):
        self.front_right_motor_enable_pin.duty_u16(self.speed)
        self.front_left_motor_enable_pin.duty_u16(self.speed)
       
        self.front_right_motor_control_1.value(1)
        self.front_right_motor_control_2.value(0)
        self.front_left_motor_control_1.value(0)
        self.front_left_motor_control_2.value(1)
        
    def left(self):
        self.front_right_motor_enable_pin.duty_u16(self.speed)
        self.front_left_motor_enable_pin.duty_u16(self.speed)
       
        self.front_right_motor_control_1.value(0)
        self.front_right_motor_control_2.value(1)
        self.front_left_motor_control_1.value(1)
        self.front_left_motor_control_2.value(0)
       
    def set_speed(self, new_speed):
        self.speed = new_speed

    def cleanUp(self):
        print("Cleaning up pins")
        self.front_right_motor_enable_pin.deinit()
        self.front_left_motor_enable_pin.deinit()
        
