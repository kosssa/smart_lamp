from machine import Pin
from umqtt.simple import MQTTClient
from drivers import SHT30
import neopixel
import time
import ubinascii
import micropython
import math
from rgbLeds import rgbLeds

import WifiConnection


rgb_light_bank = None
white_bank = None
led_quantity = 17
sampling = 16

#______________________ LED LIGHTS ______________________

pixel = rgbLeds(2, led_quantity)

#_____________________  light bulb ______________________

light_bulb = Pin(13, Pin.OUT)

#__________________  Connect to WiFi  ___________________

WifiConnection.do_connect()

#____________________  Temp & Humid _____________________

last_message = 0
message_interval = 10
counter = 0

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
sensor = SHT30()

def  read_temp_and_humid():
    temperature, humidity = sensor.measure()
    # print('Temperature:', temperature, 'ºC, RH:', humidity, '%')
    return  str(temperature), str(humidity)

#______________________   MQTT   ______________________

SERVER = '192.168.1.10'
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b'dev/test'

TOPIC_TEMPERATURE = b'smart_lamp/temp'
TOPIC_HUMIDITY = b'smart_lamp/humidity'
TOPIC_LAMP_SET_ON = b'smart_lamp/light_bulb/SetOn'
TOPIC_LAMP_GET_ON = b'smart_lamp/light_bulb/GetOn'

TOPIC_RGB_SET_ON = b'smart_lamp/rgb/SetOn'
TOPIC_RGB_GET_ON = b'smart_lamp/rgb/GetOn'

TOPIC_RGB_SET_RGB = b'smart_lamp/rgb/SetRGB'
TOPIC_RGB_GET_RGB = b'smart_lamp/rgb/GetRGB'

# msg = b'to jest pierwsza taka akcja'

state = 0
rgb_state = 0


def sub_cb(topic, msg):
    global state
    print("topic:", TOPIC_RGB_SET_ON, "\tmsg:", msg)
    if topic == TOPIC_RGB_SET_ON:
        # rgp_light_on() if msg == b"true" else rgb_light_off()
        if msg == b"true":
            pixel.on()
            client.publish(TOPIC_RGB_GET_ON, "true")
        else:
            pixel.off()
            client.publish(TOPIC_RGB_GET_ON, "false")

    elif topic == TOPIC_RGB_SET_RGB:
        #w ustawieniu koloru powinien automat sprawdzać czy nie ma nowego msg set 
        # jesli tak ma prerwać ustawienie koloru
        
        pixel.setColorFluentMode(msg)
        
        # client.publish(TOPIC_RGB_GET_RGB, msg)

    elif topic == TOPIC_LAMP_SET_ON:
        print("topic:", TOPIC_LAMP_SET_ON)
        light_bulb.on() if msg == b"true" else light_bulb.off()

def publish_light_bulb_status():
    temperature, humidity = sensor.measure()
    client.publish(TOPIC_HUMIDITY, str(humidity) + "%")
    # print('Publish light bulb status :', TOPIC_LAMP_GET_ON, " true")

def publish_temp_and_humid():
    temperature, humidity = sensor.measure()
    client.publish(TOPIC_TEMPERATURE, str(temperature))
    client.publish(TOPIC_HUMIDITY, str(humidity) + "%" )
    # print('Temperature:', temperature, 'ºC, RH:', humidity, '%')

client = MQTTClient(CLIENT_ID, SERVER, 1883, user="username", password="password")
client.set_callback(sub_cb)
client.connect()
client.subscribe(TOPIC_RGB_SET_ON)
client.subscribe(TOPIC_RGB_SET_RGB)
client.subscribe(TOPIC_LAMP_SET_ON)

client.publish(TOPIC_LAMP_GET_ON, "true")
client.publish(TOPIC_RGB_GET_ON, "true")

publish_temp_and_humid()

# print("Connected to %s, subscribed to %s topic" % (SERVER, TOPIC_LAMP_ON))


try:
    while True:
        # print(micropython.mem_info())
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            publish_temp_and_humid()
            last_message = time.time()
        # time.sleep(0.01)
finally:
    client.disconnect()


