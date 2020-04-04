#
#   main.py
#

import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime
from tasks import *

# set the logging level
LOG_LEVEL = logging.INFO

def main():
    # setup logging
    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)
    
    loop = asyncio.get_event_loop()
    # set max_workers to 1 to prevent multiple jobs occurring at once
    executor = ThreadPoolExecutor(max_workers=1)
    loop.set_default_executor(executor)
    event = asyncio.Event()
    event.clear()
    
    # schedule task execution
    asyncio.run(schedule_tasks(loop, event))
    loop.run_forever()

if __name__ == "__main__":
    main()
