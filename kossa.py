import time
from machine import Pin
from WifiConnection import WifiConnection
from RgbLeds import RgbLeds
from drivers import SHT30
print("Smart lamp is loading...")

#RgbLeds(<GPIO_pin>, <led_quantity>, <max_power_source>)
pixel = RgbLeds(2, 43, 900)


my_Wifi = WifiConnection()
my_Wifi.connect()

light_bulb = Pin(13, Pin.OUT)

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
sensor = SHT30()

while True:
    print(my_Wifi.isconnected())
    print(sensor.measure())
    print(sensor.measure_int())
    time.sleep(3)
