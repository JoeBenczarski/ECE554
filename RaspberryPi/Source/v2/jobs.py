#
#   jobs.py
#

import asyncio

import logging
from datetime import datetime

from light_services import *


class job(object):

    def __init__(self, raw_str):
        self.servs = light_service()
        arr = raw_str.split(';')
        arr.pop()                     # remove empty entry
        self.cmd = str(arr.pop(0))    # get command
        self.leds = int(arr.pop(0))   # get num leds
        self.freq = float(arr.pop(0)) # get frequency
        self.colors = []
        for i in arr:
            rgb = i.split(',')
            self.colors.append((int(rgb[0]), int(rgb[1]), int(rgb[2])))

    def process(self, light_services, event):
        # log the processing
        logging.info("{t}       job::process() processing job".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        # execute the service
        light_services.run(self.cmd, self.leds, self.freq, self.colors, event)
        logging.info("{t}       job::process() job finished".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
