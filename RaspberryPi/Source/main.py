#
#   main.py
#


import asyncio
import logging
from datetime import datetime
from Source.tasks import schedule_tasks


# set the logging level
LOG_LEVEL = logging.INFO


def main():
    # setup logging
    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

    # schedule task execution
    asyncio.run(schedule_tasks())


if __name__ == "__main__":
    main()
