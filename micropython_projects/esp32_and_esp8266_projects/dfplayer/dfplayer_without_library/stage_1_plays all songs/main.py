import machine
from machine import Pin
import utime
from utime import sleep

DFPLAYER_UART = machine.UART(1, baudrate=9600, tx=17, rx=16)


def send_command(command, parameter=0):
    query = bytes([0x7E, 0xFF, 0x06, command, 0x00, 0x00, parameter, 0xEF])
    DFPLAYER_UART.write(query)


def main():

    send_command(0x0D)

    send_command(0x16)


if __name__ == "__main__":
    main()
