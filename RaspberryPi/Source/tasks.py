#
#   tasks.py
#


import asyncio
import logging
from bluetooth import bluetooth
from datetime import datetime


# 1 ms definition
ONE_MS = 0.001

# lock for job access
job_lock = asyncio.Lock()


async def idle_handler():
    while True:
        # log the handler execution
        #logging.info("{t}       Executing idle_handler()".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # run every 10ms
        await asyncio.sleep(10*ONE_MS)


async def bluetooth_handler(bt):
    while True:
        # log the handler execution
        logging.info("{t}       Executing bluetooth_handler()".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # check for incoming bluetooth messages
        bt.rx_check()

        # TODO - create lighting job from message
        async with job_lock:
            if bt.last_msg != None:
                pass

        # run every 100ms
        await asyncio.sleep(100*ONE_MS)


async def lighting_handler():
    while True:
        # log the handler execution
        logging.info("{t}       Executing lighting_handler()".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # TODO - process any lighting jobs
        async with job_lock:
            pass

        # run every 100ms
        await asyncio.sleep(100*ONE_MS)


async def run_tasks():
    bt = bluetooth()

    # create tasks
    tasks = []
    tasks.append(asyncio.create_task(idle_handler()))
    tasks.append(asyncio.create_task(bluetooth_handler(bt)))
    tasks.append(asyncio.create_task(lighting_handler()))

    # schedule tasks
    for task in tasks:
        await task
