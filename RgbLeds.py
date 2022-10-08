from machine import Pin
import neopixel
import time
import math
# stworzenie konstruktora powinno wykonac małą prezentacje/najporostrzy efekt
# jak w zegarach auta rozjaśnienie diód od pierwszej do ostatniej i wyaszenie w odwrotnej kolejności


# pomysł na przyszłość:
#     jak jest używany jeden z kolorów(tak mniej wiecej) to można by wtedy podbić moc ale do tego ficzera wymagany bedzie amperowmierz i woltomierz żeby sprawdzic czy zailacz nie dziala na 100%

class RgbLeds:

    def __init__(self, gpioPin, led_quantity, max_amper):
        self.led_quantity = led_quantity
        self.rgb = neopixel.NeoPixel(Pin(gpioPin), led_quantity)
        print("Neopixel Configured:( GPIO=", gpioPin, "led quantity=", led_quantity)
        self.rgb.state = None
        self.rgb.last_state = None
        self.sampling = 16
        self._erase_leds()
        self._calculate_power_factor(max_amper, led_quantity)

    def _calculate_power_factor(self, max_amperage, led_quantity):
        one_diode_power = 60
        self.power_factor = max_amperage/(one_diode_power*led_quantity)
        print("self.power_factor")
        print(self.power_factor)

    def status(self):
        if self.rgb.state:
            return True
        return False

    def on(self):
        for i in range(0, self.led_quantity):
            self.rgb[i] = self.rgb.last_state[i] if self.rgb.last_state else (255, 255, 255)
        self.rgb.write()
        self.save_rgb_state()
        self.rgb.state = True

    def off(self):
        self.save_rgb_state()
        self._erase_leds()
        self.rgb.state = None

    def _erase_leds(self):
        print("wylaczamy swiatelka")
        for i in range(0, self.led_quantity):
            self.rgb[i] = (0, 0, 0)
        self.rgb.write()

    def save_rgb_state(self):
        self.rgb.last_state = list()
        for i in range(0, self.led_quantity):
            self.rgb.last_state.append(self.rgb[i])
        print("Last state: ", self.rgb.last_state)

    def read_color(self):
        if self.rgb.last_state:
            red, green, blue = self.rgb.last_state[0]
            print("red, green, blue = ", red, green, blue)
            return red, green, blue
        # print("!!! return None color !!!")
        return None

    def set_color(self, red, green, blue):
        red, green, blue = self._decrease_power(red, green, blue)
        print("red, green, blue: ", red, green, blue)
        for i in range(0, self.led_quantity):
            self.rgb[i] = (int(red), int(green), int(blue))
        if self.rgb.state:
            self.rgb.write()
        # time.sleep(0.01)

    def _decrease_power(self, r, g, b):
        r = r * self.power_factor
        g = g * self.power_factor
        b = b * self.power_factor
        return r, g, b

    def _set_color_fluent_mode(self, msg):
        # check initial color
        
        redi, greeni, bluei = self.read_color() if self.read_color() else (0,0,0)
        redi, greeni, bluei = float(redi), float(greeni), float(bluei)
        
        red, green, blue = msg.decode('ascii').split(",")
        red, green, blue = float(red), float(green), float(blue)
        delta_r = redi - red
        delta_g = greeni - green
        delta_b = bluei - blue
        # print("red, green, blue = ", red, green, blue)
        # print("redi, greeni, bluei = ", redi, greeni, bluei)
        # print("delta_r, delta_g, delta_b = ", delta_r, delta_g, delta_b)
        
        delta_ru = delta_r/self.sampling
        delta_gu = delta_g/self.sampling
        delta_bu = delta_b/self.sampling
        # print("delta_ru, delta_gu, delta_bu = ", delta_ru, delta_gu, delta_bu)

        if self.rgb.state:
            for i in range(0, self.sampling-1):
                redi = redi - delta_ru
                greeni = greeni - delta_gu
                bluei = bluei - delta_bu
                print("redi, greeni, bluei = ", redi, greeni, bluei)
                self.set_color(redi, math.floor(greeni), math.floor(bluei))
        self.set_color(red, green, blue)
        self.save_rgb_state()
        print("color sets to:", red, green, blue )
        
# pixel = rgbLeds(2, led_quantity)
# pixel.on()
# pixel._set_color_fluent_mode(b"255,0,0")
# time.sleep(.5)
# pixel.read_color()
# print("\n\n\n\n\n\n\n")
# # pixel.set_color(0,255,0)
# pixel._set_color_fluent_mode(b'0,0,255')
# pixel.read_color()
# # pixel.save_rgb_state()
# # pixel.read_color()
# pixel.off()



