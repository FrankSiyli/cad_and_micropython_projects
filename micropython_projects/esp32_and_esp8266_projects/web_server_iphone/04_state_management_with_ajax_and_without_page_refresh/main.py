import time
import uasyncio

counter = 1

try:
    import usocket as socket
except ImportError:
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


def web_page():
    global counter
    counter += 1
    html = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"""
    html += (
        """<html><head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
         <script>
        function updateCounter() {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    document.getElementById("counter").innerHTML = this.responseText;
                }
            };
            xhttp.open("GET", "/counter", true);
            xhttp.send();
        }
        // Update counter every 5 seconds
        setInterval(updateCounter, 1000);
        </script>
    </head>
  <body><h1> <span id="counter">"""
        + "Counter: "
        + str(counter)
        + """</span></h1></body></html>"""
    )
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 80))
s.listen(5)


async def handle_client(reader, writer):
    request = await reader.read(1024)
    response = web_page()
    await writer.awrite(response)
    await writer.aclose()


async def main():
    while True:
        conn, addr = s.accept()
        print("Got a connection from %s" % str(addr))
        request = conn.recv(1024)
        print("Content = %s" % str(request))
        response = web_page()
        conn.send(response)
        conn.close()


uasyncio.run(main())
