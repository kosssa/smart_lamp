import time
# import micropython
from WifiConnection import WifiConnection
#
my_Wifi = WifiConnection()
my_Wifi.connect()
# print(WifiConnection.x)
print("hello My Big world")
while True:
    print(my_Wifi.isconnected())
    time.sleep(3)
