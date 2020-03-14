#
#   bluetooth.py
#

import logging
from datetime import datetime


class bluetooth:

    def __init__(self):
        # log object initialization
        logging.info("{t}       Executing bluetooth::__init__()".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # init object variables
        self.last_msg = None


    def rx_check(self):
        # log function execution
        logging.info("{t}       Executing bluetooth::rx_check()".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # TODO - check for a received bluetooth message
        self.last_msg = "TOOGLE 1"
