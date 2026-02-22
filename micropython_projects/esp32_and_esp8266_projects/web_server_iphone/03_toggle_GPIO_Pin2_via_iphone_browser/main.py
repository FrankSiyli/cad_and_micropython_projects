from machine import Pin

try:
    import usocket as socket
except:
    import socket

import network
import esp

esp.osdebug(None)
import gc

gc.collect()

ssid = "MicroPython"
password = "12345678"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

while not ap.active():
    pass

print("Connection successful")
print(ap.ifconfig())

led = Pin(2, Pin.OUT)


def generate_web_page():
    html = """HTTP/1.1 200 OK\nContent-Type: text/html\n\n"""
    html += """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{padding: 3vh;}p{font-size: 1.2rem;}
    .button{display: inline-block; color: #fff; background-color: #1c1c1c; border-radius: 10px; padding: 12px 35px; text-decoration: none; font-size: 20px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
    <p><a href="/?led=on"><button class="button">Pin 2 ON</button></a></p>
    <p><a href="/?led=off"><button class="button button2">Pin 2 OFF</button></a></p></body></html>"""
    return html


def handle_request(request):
    led_on = request.find("/?led=on")
    led_off = request.find("/?led=off")
    if led_on == 6:
        print("LED ON")
        led.value(1)
    elif led_off == 6:
        print("LED OFF")
        led.value(0)


def run_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print("Got a connection from %s" % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print("Content = %s" % request)
        handle_request(request)
        response = generate_web_page()
        conn.send(response)
        conn.close()


run_server()
