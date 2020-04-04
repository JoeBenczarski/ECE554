#
# light_services.py
#

import time
import RPi.GPIO as GPIO
 
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
 
# Configure the count of pixels:
PIXEL_COUNT = 32
    
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0

class light_service(object):    

    def __init__(self):
        self.services = {
            'Off': self.off,
            'Solid': self.solid,
            'Pulse': self.pulse,
            'Shift Left': self.shift_left,
            'Shift Right': self.shift_right
        }
        self.pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
        
    def run(self, service_name, *args):
        self.services[service_name](*args)
    
    # Set the lights to rainbow color
    def shift_left(self, leds=1, freq=0, colors=[(255,255,255)]):
        pass

    # Set the lights to rainbow color
    def shift_right(self, leds=1, freq=0, colors=[(255,255,255)]):
        pass
    
    # Set the lights to pulse a color for a duration and frequency
    def pulse(self, leds=1, freq=0, colors=[(255,255,255)]):
        for color in colors:
            self.pixels.set_pixels(self._RGB_to_color(color))
            self.pixels.show()
            time.sleep(freq)

    # Set the lights to a color and brightness
    def solid(self, leds=1, freq=0, colors=[(255,255,255)]):
        lights = self.pixels.count()
        count = 0
        while count < lights:
            for color in colors:
                for i in range(leds):
                    if count >= lights:
                        break
                    self.pixels.set_pixel(count, self._RGB_to_color(color))
                    count = count+1
        self.pixels.show()
    
    # Set the lights off
    def off(self, leds=1, freq=0, colors=[(255,255,255)]):
        self.pixels.clear()
        self.pixels.show()
        
    # Return separate R, G, B values from a RGB tuple
    def _get_rgb(self, tup):
        return tup[0], tup[1], tup[2]
    
    # Scale the rgb values (brightness)
    def _rgb_scale(self, rgb, scale):
        r, g, b = self._get_rgb(rgb)
        return (r*scale, g*scale, b*scale)

    # Wrapper function for ensuring proper request
    def _RGB_to_color(self, rgb):
        # lib requires int
        r, g, b = self._get_rgb(rgb)
        # lib actually requires BGR instead of RGB
        return Adafruit_WS2801.RGB_to_color(int(b), int(g), int(r))

    # Define the wheel function to interpolate between different hues.
    def _wheel(self, pos):
        if pos < 85:
            return self._RGB_to_color((pos * 3, 255 - pos * 3, 0))
        elif pos < 170:
            pos -= 85
            return self._RGB_to_color((255 - pos * 3, 0, pos * 3))
        else:
            pos -= 170
            return self._RGB_to_color((0, pos * 3, 255 - pos * 3))
