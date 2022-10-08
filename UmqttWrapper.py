import machine
import ubinascii
from RgbLeds import RgbLeds


class UmqttWrapper(RgbLeds):

    def __init__(self, server):
        # SERVER = '192.168.1.10'
        self.server_ip = '192.168.1.10'
        print("machine_unique_id")
        print(machine.unique_id())
        self.client_id = ubinascii.hexlify(machine.unique_id())
        self._config_topics()

    def _config_topics(self):
        self.topic_temperature = b'smart_lamp/temp'
        self.topic_humidity = b'smart_lamp/humidity'
        self.topic_light_bulb_set_on = b'smart_lamp/light_bulb/SetOn'
        self.topic_light_bulb_get_on = b'smart_lamp/light_bulb/GetOn'
        self.topic_rgb_set_on = b'smart_lamp/rgb/SetOn'
        self.topic_rgb_get_on = b'smart_lamp/rgb/GetOn'
        self.topic_rgb_set_rgb = b'smart_lamp/rgb/SetRGB'
        self.topic_rgb_get_rgb = b'smart_lamp/rgb/GetRGB'

    def hello_world(self):
        print("hello_world")

    def callback(self, topic, msg):
        print("topic:", topic, "\tmsg:", msg)
        if topic == self.topic_rgb_set_on:
            # rgp_light_on() if msg == b"true" else rgb_light_off()
            if msg == b"true":
                RgbLeds.on()
                self.client.publish(TOPIC_RGB_GET_ON, "true")
            else:
                pixel.off()
                client.publish(TOPIC_RGB_GET_ON, "false")

        elif topic == TOPIC_RGB_SET_RGB:
            # w ustawieniu koloru powinien automat sprawdzać czy nie ma nowego msg set
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
        client.publish(TOPIC_HUMIDITY, str(humidity) + "%")
        # print('Temperature:', temperature, 'ºC, RH:', humidity, '%')


SERVER = '192.168.1.10'
CLIENT_ID = ubinascii.hexlify(machine.unique_id())


client = MQTTClient(CLIENT_ID, SERVER, 1883, user="username", password="password")
client.set_callback(sub_cb)
client.connect()
client.subscribe(TOPIC_RGB_SET_ON)
client.subscribe(TOPIC_RGB_SET_RGB)
client.subscribe(TOPIC_LAMP_SET_ON)

client.publish(TOPIC_LAMP_GET_ON, "true")
client.publish(TOPIC_RGB_GET_ON, "true")

publish_temp_and_humid()
