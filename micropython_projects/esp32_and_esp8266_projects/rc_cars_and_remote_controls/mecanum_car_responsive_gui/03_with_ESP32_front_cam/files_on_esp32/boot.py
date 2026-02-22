import network, utime

PRIMARY_SSID = "ssid"
PRIMARY_PASSWORD = "ssid password"



def do_connect():
    import network

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("connecting to network...")
        sta_if.active(True)
        sta_if.connect(PRIMARY_SSID, PRIMARY_PASSWORD)
        while not sta_if.isconnected():
            pass
    print("Connected! Network config:", sta_if.ifconfig())


print("Connecting to your wifi...")
do_connect()

