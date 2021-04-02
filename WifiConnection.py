import network
sta_if = network.WLAN(network.STA_IF)

def do_connect():
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Hosse321', 'S57C2V3MDVDF$#%@')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())