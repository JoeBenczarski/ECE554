#
# light_services.py
#

import asyncio

import logging
from datetime import datetime

import time
import RPi.GPIO as GPIO
 
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

from reverse_util import *
 
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
        self.size = self.pixels.count()
        
    def run(self, service_name, *args):
        logging.info("{t}       light_service::run() looking up service".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        self.services[service_name](*args)
        logging.info("{t}       light_service::run() returned from service".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        
    
    # Shift lights to the left
    def shift_left(self, leds=1, freq=0, colors=[(255,255,255)], event=None):
        logging.info("{t}       light_service::shift_left() running".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        colors = self._get_rgb_list(self.size, leds, colors)
        self._set_all_pixels(colors)
        while True:
            if event.is_set():
                logging.info("{t}       light_service::shift_left() event is set".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
                break
            time.sleep(freq/2)
            rotate_left(colors, 1)
            self._set_all_pixels(colors)
        logging.info("{t}       light_service::shift_left() stopped".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        
    # Shift lights to the right
    def shift_right(self, leds=1, freq=0, colors=[(255,255,255)], event=None):
        logging.info("{t}       light_service::shift_right() running".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        colors = self._get_rgb_list(self.size, leds, colors)
        self._set_all_pixels(colors)
        while True:
            if event.is_set():
                logging.info("{t}       light_service::shift_right() event is set".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
                break
            time.sleep(freq/2)
            rotate_right(colors, 1)
            self._set_all_pixels(colors)
        logging.info("{t}       light_service::shift_right() stopped".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
    
    # Set the lights to pulse a color for a duration and frequency
    def pulse(self, leds=1, freq=0.2, colors=[(255,255,255)], event=None):
        logging.info("{t}       light_service::pulse() running".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        while True:
            if event.is_set():
                logging.info("{t}       light_service::pulse() event is set".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
                break
            for color in colors:
                self.pixels.set_pixels(self._RGB_to_color(color))
                self.pixels.show()
                time.sleep(freq/2)
        logging.info("{t}       light_service::pulse() stopped".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

    # Set the lights to a color and brightness
    def solid(self, leds=1, freq=0, colors=[(255,255,255)], event=None):
        logging.info("{t}       light_service::solid() running".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        # get list of colors
        colors = self._get_rgb_list(self.size, leds, colors)
        self._set_all_pixels(colors)
        logging.info("{t}       light_service::solid() stopped".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

    # Set the lights off
    def off(self, leds=1, freq=0, colors=[(255,255,255)], event=None):
        logging.info("{t}       light_service::off() running".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        self.pixels.clear()
        self.pixels.show()
        logging.info("{t}       light_service::off() stopped".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
    
    # rotate an array in place to the left
    def _rotate_left(self, arr, shift=1):
        pass
    
    # rotate an array in place to the right
    def _rotate_right(self, arr, shift=1):
        pass
        
    # Set all LEDs in strip
    def _set_all_pixels(self, colors=[(255,255,255)]):
        # get list of colors
        for i in range(self.size):
            self.pixels.set_pixel(i, self._RGB_to_color(colors[i]))
        self.pixels.show()
    
    # Get an array of colors based on size, leds, and colors
    def _get_rgb_list(self, size=32, leds=1, colors=[(255,255,255)]):
        rgb_list = []
        count = 0
        while count < size:
            for color in colors:
                for i in range(leds):
                    if count >= size:
                        break
                    rgb_list.append(color)
                    count += 1
        return rgb_list
            
    
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
