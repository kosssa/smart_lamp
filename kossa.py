import time
import micropython
from machine import Pin
from WifiConnection import WifiConnection
from RgbLeds import RgbLeds
from drivers import SHT30

from UmqttWrapper import UmqttWrapper

print("Smart lamp is loading...")

pixel = RgbLeds(2, 43, 900)

my_Wifi = WifiConnection()
my_Wifi.connect()

light_bulb = Pin(13, Pin.OUT)
light_bulb.off()

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
temp_sensor = SHT30()
server_ip = '192.168.1.10'
mqtt = UmqttWrapper(server_ip, pixel, temp_sensor, light_bulb)
mqtt.connect()
mqtt.subscribe_rgb_and_light_bulb()
mqtt.publish_all_sensor_and_lights()
mqtt.publish_temp_and_humid()

last_message = 0
message_interval = 3
print(micropython.mem_info())
try:
    while True:
        mqtt.client.check_msg()
        if (time.time() - last_message) > message_interval:
            # mqtt.publish_temp_and_humid()
            # mqtt.publish_last_rgb_state()
            last_message = time.time()
        time.sleep(0.01)
finally:
    mqtt.client.disconnect()
