#
#   main.py
#


import asyncio
import logging
from datetime import datetime
from tasks import run_tasks


# set the logging level
LOG_LEVEL = logging.INFO


def main():
    # setup logging
    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

    # start task execution
    asyncio.run(run_tasks())


if __name__ == "__main__":
    main()
