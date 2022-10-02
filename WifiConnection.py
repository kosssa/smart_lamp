import network
import time
wifi = network.WLAN(network.STA_IF)


class WifiConnection:
    def __init__(self):
        self.wifi = network.WLAN(network.STA_IF)

    def isconnected(self):
        return wifi.isconnected()

    def connect(self):
        if not wifi.isconnected():
            print('connecting to network...')
            wifi.active(True)
            wifi.connect('Hosse321', 'S57C2V3MDVDF$#%@')
            while not wifi.isconnected():
                print("wifi not connected, waiting ....")
                time.sleep(1)
        print('network config:', wifi.ifconfig())

    def reconet_to_wifi(self):
        for x in range(5):
            time.sleep(x)
            if wifi.isconnected():
                break

        while wifi.isconnected():
            time.sleep(2)

        if not wifi.isconnected():
            time.sleep(2)
