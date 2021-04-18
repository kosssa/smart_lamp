from machine import Pin
import neopixel
import time
import math

class rgbLeds:
    def __init__(self, gpioPin, ledQuantity):
        self.ledQuantity = ledQuantity
        self.rgb = neopixel.NeoPixel(Pin(gpioPin), ledQuantity)
        print("Neopixel Configured:( GPIO=", gpioPin, "led quantity=", ledQuantity)
        self.rgb.write()
        self.rgb.state = None
        self.rgb.last_state = None
        self.sampling = 16
    
    def status(self):
        if self.rgb.state:
            return True
        return False

    def on(self):
        for i in range(0, self.ledQuantity):
            self.rgb[i] = self.rgb.last_state[i] if self.rgb.last_state else (255, 255, 255)
        self.rgb.write()
        self.saveState()
        self.rgb.state = True

    def off(self):
        self.saveState()
        self._eraseLeds()
        self.rgb.state = None

    def _eraseLeds(self):
        print("wylaczamy swiatelka")
        for i in range(0, self.ledQuantity):
            self.rgb[i] = (0, 0, 0)
        self.rgb.write()

    def saveState(self):
        self.rgb.last_state = list()
        for i in range(0, self.ledQuantity):
            self.rgb.last_state.append(self.rgb[i])
        print("Last state: ", self.rgb.last_state)

    def readColor(self):
        if self.rgb.last_state:
            red, green, blue = self.rgb.last_state[0]
            print("red, green, blue = ", red, green, blue)
            return red, green, blue
        # print("!!! return None color !!!")
        return None

    def setColor(self, red, green, blue):
        print("red, green, blue: ",red, green, blue)
        for i in range(0, self.ledQuantity):
            self.rgb[i] = (int(red), int(green), int(blue))
        if self.rgb.state:
            self.rgb.write()
        # time.sleep(0.01)

    def setColorFluentMode(self, msg): 
        # check initial color
        
        redi, greeni, bluei = self.readColor() if self.readColor() else (0,0,0)
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
                self.setColor(redi, math.floor(greeni), math.floor(bluei))        
        self.setColor(red, green, blue)
        self.saveState()
        print("color sets to:", red, green, blue )
        
# pixel = rgbLeds(2, led_quantity)
# pixel.on()
# pixel.setColorFluentMode(b"255,0,0")
# time.sleep(.5)
# pixel.readColor()
# print("\n\n\n\n\n\n\n")
# # pixel.setColor(0,255,0)
# pixel.setColorFluentMode(b'0,0,255')
# pixel.readColor()
# # pixel.saveState()
# # pixel.readColor()
# pixel.off()



