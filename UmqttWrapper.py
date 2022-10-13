import time

import machine
import ubinascii
from umqtt.simple import MQTTClient
# from RgbLeds import RgbLeds


class UmqttWrapper:

    def __init__(self, server, rgb_leds, temp_sensor, light_bulb):
        # SERVER = '192.168.1.10'
        self.server_ip = server
        print("machine_unique_id")
        print(machine.unique_id())
        #spróbować użyc randomowego profixu bo może przy połaczeniu do brokera dany id juz jest polaczony (zerwane połaczenie)
        self.client_id = ubinascii.hexlify(machine.unique_id())
        self._config_topics()
        self.rgb_leds = rgb_leds
        self.temp_sensor = temp_sensor
        self.light_bulb = light_bulb
        self.client = None

    def _config_topics(self):
        self.topic_temperature = b'smart_lamp/temp'
        self.topic_humidity = b'smart_lamp/humidity'
        self.topic_light_bulb_set_on = b'smart_lamp/light_bulb/SetOn'
        self.topic_light_bulb_get_on = b'smart_lamp/light_bulb/GetOn'
        self.topic_rgb_set_on = b'smart_lamp/rgb/SetOn'
        self.topic_rgb_get_on = b'smart_lamp/rgb/GetOn'
        self.topic_rgb_set_rgb = b'smart_lamp/rgb/SetRGB'
        self.topic_rgb_get_rgb = b'smart_lamp/rgb/GetRGB'

    def connect(self):
        i = 0
        while i < 30:
            try:
                self.client = MQTTClient(self.client_id, self.server_ip, 1883, user="username", password="password")
                self.client.set_callback(self.callback)
                self.client.connect()
                break
            except:
                print("can't connect to mqqt broker")
            i += 1
            time.sleep(10)

    def subscribe_rgb_and_light_bulb(self):
        self.client.subscribe(self.topic_rgb_set_on)
        self.client.subscribe(self.topic_rgb_set_rgb)
        self.client.subscribe(self.topic_light_bulb_set_on)

    def publish_all_sensor_and_lights(self):
        self.client.publish(self.topic_light_bulb_get_on, "false")
        self.client.publish(self.topic_rgb_get_on, "false")
        self.publish_temp_and_humid()

    def hello_world(self):
        print("hello_world")

    def callback(self, topic, msg):
        print("topic:", topic, "\tmsg:", msg)
        if topic == self.topic_rgb_set_on:
            if msg == b"true":
                self.rgb_leds.on()
                self.client.publish(self.topic_rgb_get_on, "true")
            else:
                self.rgb_leds.off()
                self.client.publish(self.topic_rgb_get_on, "false")

        elif topic == self.topic_rgb_set_rgb:
            # ToDo
            # check if new msg is arrived, if yes return and set colort again
            self.rgb_leds.set_color_from_msg(msg)
            # self.client.publish(self.topic_rgb_get_rgb, msg) <- this generate the issue
            # (color was change to white when slide goes to 0 )

        elif topic == self.topic_light_bulb_set_on:
            print("topic:", self.topic_light_bulb_set_on)
            if msg == b"true":
                self.light_bulb.on()
                self.client.publish(self.topic_light_bulb_get_on, "true")
            else:
                self.light_bulb.off()
                self.client.publish(self.topic_light_bulb_get_on, "false")

    def publish_temp_and_humid(self):
        temperature, humidity = self.temp_sensor.measure()
        self.client.publish(self.topic_temperature, str(temperature))
        self.client.publish(self.topic_humidity, str(humidity) + "%")
        print('Temperature:', temperature, 'C \thumidity:', humidity, '%')

    def publish_last_rgb_state(self):
        if self.rgb_leds.last_state_ascii:
            print(self.rgb_leds.last_state_ascii)
            self.client.publish(self.topic_rgb_get_rgb,  self.rgb_leds.last_state_ascii)
