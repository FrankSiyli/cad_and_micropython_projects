import time

counter = 1

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

while ap.active() == False:
    pass

print("Connection successful")
print(ap.ifconfig())


# content="10" in head tag sets the refresh interval
def web_page(counter):
    html = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"""
    html += (
        """<html><head>
        <meta http-equiv="refresh" content="10">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
  <body><h1>Counter: """
        + str(counter)
        + """</h1></body></html>"""
    )
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print("Content = %s" % str(request))
    response = web_page(counter)
    conn.send(response)
    conn.close()
    counter += 1
