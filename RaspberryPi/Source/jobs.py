#
#   jobs.py
#

from datetime import datetime
import logging


class job(object):
    def __init__(self, *args):
        self.cmd = None
        self.data = []

    def process(self):
        logging.info("{t}       job::process() processing job".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        pass
