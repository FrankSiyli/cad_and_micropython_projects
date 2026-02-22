import machine
from machine import Pin, I2C, ADC
import utime
from utime import sleep
import ssd1306

i2c = I2C(0, sda=Pin(4), scl=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

adc = ADC(Pin(14))
adc.atten(ADC.ATTN_11DB)


def update_display(voltage):
    oled.fill(0)
    voltage_str = "{:.2f}".format(voltage)
    oled.text("Voltage: {}V".format(voltage_str), 10, 20)

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
    utime.sleep_ms(100)
    adc_value = adc.read()
    voltage = adc_value * (3.3 / 4095) * 2 + 0.34
    return voltage


def main():
    global battery_voltage
    battery_voltage = read_battery_voltage()

    update_display(battery_voltage)


if __name__ == "__main__":
    main()
