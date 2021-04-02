from machine import Pin
from umqtt.simple import MQTTClient
from drivers import SHT30
import neopixel
import time
import ubinascii
import micropython
import math
rgb_light_bank = None
white_bank = None
led_quantity = 17
sampling = 16

#_________________ LED LIGHTS ________________

np = neopixel.NeoPixel(Pin(2), led_quantity)
np.write()


def rgb_light_save_state():
    global rgb_light_bank
    rgb_light_bank = list()
    for i in range(0, led_quantity):
        rgb_light_bank.append(np[i])
    print("rgb_light_bank: ", rgb_light_bank)


def erase_leds():
    for i in range(0, led_quantity):
        np[i] = (0, 0, 0)
    np.write()

def read_current_color():
    global rgb_light_bank
    if rgb_light_bank:
        red, green, blue = rgb_light_bank[0]
        # print("red, green, blue = ", red, green, blue)
        return red, green, blue
    print("!!!!!!!!!!!!   jestesmy w else   !!!!!!!!")
    # jesli jestesmy tutaj to r g b = 0 0 0
    return 0, 0, 0


def set_light_set_color_initial(msg):
    global sampling
    redi, greeni, bluei = read_current_color()
    red, green, blue = msg.decode('ascii').split(",")

    delta_r = int(red) - redi
    delta_g = int(green) - greeni
    delta_b = int(blue) - bluei
    # print("red, green, blue = ", red, green, blue)
    # print("redi, greeni, bluei = ", redi, greeni, bluei)
    # print("delta_r, delta_g, delta_b = ", delta_r, delta_g, delta_b)
    delta_ru = math.floor(delta_r/sampling)
    delta_gu = math.floor(delta_g/sampling)
    delta_bu = math.floor(delta_b/sampling)
    # print("delta_ru, delta_gu, delta_bu = ", delta_ru, delta_gu, delta_bu)

    for i in range(1, sampling + 1):
        print("i=", i)
        rgb_light_set_color_2(i*delta_ru + redi, i * delta_gu + greeni, i* delta_bu + bluei)



def rgb_light_set_color_2(red, green, blue):
    print("rgb_light_set_color_2: ", red, green, blue)
    for i in range(0, led_quantity):
        np[i] = (red, green, blue)
        # print("rgb_light_set_color: ", np[i])
    np.write()

def rgb_light_set_color(msg):
    red, green, blue = msg.decode('ascii').split(",")
    print("rgb_light_bank: ", rgb_light_bank)
    for i in range(0, led_quantity):
        np[i] = (int(red), int(green), int(blue))
        # print("rgb_light_set_color: ", np[i])
    print("color sets to:", red, green, blue )
    np.write()

def rgb_light_add_white(msg):
    white_level = msg.decode('ascii')
    for i in range(0, led_quantity):
        np[i] = (int(red), int(green), int(blue))
        print("rgb_light_set_color: ", np[i])
    np.write()

def rgp_light_on():
    global rgb_state
    global rgb_light_bank
    for i in range(0, led_quantity):
        np[i] = rgb_light_bank[i] if rgb_light_bank else (0, 0, 0)
    np.write()
    rgb_light_save_state()
    rgb_state = 1

def rgb_light_off():
    rgb_light_save_state()
    erase_leds()

#________________  light bulb ________________

light_bulb = Pin(13, Pin.OUT)


#________________  Temp & Humid _______________

last_message = 0
message_interval = 3
counter = 0

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
sensor = SHT30()

def  read_temp_and_humid():
    temperature, humidity = sensor.measure()
    print('Temperature:', temperature, 'ºC, RH:', humidity, '%')
    return  str(temperature), str(humidity)

#________________     MQTT    ________________
SERVER = '192.168.1.10'
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b'dev/test'

TOPIC_TEMPERATURE = b'smart_lamp/temp'
TOPIC_HUMIDITY = b'smart_lamp/humidity'
TOPIC_LAMP_ON = b'smart_lamp/light_bulb'
TOPIC_LAMP_GET_ON = b'smart_lamp/light_bulb/GetOn'

TOPIC_RGB_ON = b'smart_lamp/SetON'
TOPIC_RGB_SET = b'smart_lamp/SetRGB'
msg = b'to jest pierwsza taka akcja'

state = 0
rgb_state = 0


def sub_cb(topic, msg):
    global state
    print((topic, msg))
    if topic == TOPIC_RGB_ON:
        print("topic:", TOPIC_RGB_ON)
        rgp_light_on() if msg == b"true" else rgb_light_off()
    elif topic == TOPIC_RGB_SET:
        print("topic:", TOPIC_LAMP_ON)
        print("msg:", msg)
        read_current_color()
        set_light_set_color_initial(msg)
        rgb_light_save_state()
    elif topic == TOPIC_LAMP_ON:
        print("topic:", TOPIC_LAMP_ON)
        light_bulb.on() if msg == b"true" else light_bulb.off()

def publish_light_bulb_status():
    temperature, humidity = sensor.measure()
    client.publish(TOPIC_LAMP_GET_ON, "true")
    client.publish(TOPIC_HUMIDITY, str(humidity) + "%")
    # print('Publish light bulb status :', TOPIC_LAMP_GET_ON, " true")

def publish_temp_and_humid():
    temperature, humidity = sensor.measure()
    client.publish(TOPIC_TEMPERATURE, str(temperature))
    client.publish(TOPIC_HUMIDITY, str(humidity) + "%" )
    print('Temperature:', temperature, 'ºC, RH:', humidity, '%')

client = MQTTClient(CLIENT_ID, SERVER, 1883, user="username", password="password")
client.set_callback(sub_cb)
client.connect()
client.subscribe(TOPIC_RGB_ON)
client.subscribe(TOPIC_RGB_SET)
client.subscribe(TOPIC_LAMP_ON)
print("Connected to %s, subscribed to %s topic" % (SERVER, TOPIC_LAMP_ON))


try:
    while True:
        # print(micropython.mem_info())
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            publish_light_bulb_status()
            publish_temp_and_humid()
            last_message = time.time()
        # time.sleep(0.01)
finally:
    client.disconnect()


