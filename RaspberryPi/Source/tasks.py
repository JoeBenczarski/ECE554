#
#   tasks.py
#

import asyncio
from datetime import datetime
import logging
from jobs import *
from sock_server import *


# 1 ms definition
ONE_MS = 0.001

# task execution period
IDLE_PERIOD      = 10*ONE_MS
BLUETOOTH_PERIOD = 150*ONE_MS
LIGHTING_PERIOD  = 100*ONE_MS

# Job queue
jobQueue = asyncio.Queue(10)
# Lock for job queue
jobLock = asyncio.Lock()


async def idle_coro():
    while True:
        # log the handler execution
        #logging.info("{t}       Executing idle_coro()".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # run every X ms
        await asyncio.sleep(IDLE_PERIOD)


async def bluetooth_coro():
    #ip_addr = '127.0.0.1'
    ip_addr = ''
    ip_port = 65432
    bt_addr = '9c:b6:d0:c3:26:e8'
    bt_port = 3

    bt_server = sock_server(ip_addr, ip_port)
    while True:
        # log the handler execution
        logging.info("{t}       Executing bluetooth_coro()".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # blocking call to wait for incoming messages
        bt_msg = await bt_server.get()

        # get a bluetooth message without blocking
        if bt_msg != None:
            async with jobLock:
                logging.info("{t}       bluetooth_coro() has job fifo lock".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
                # add job to queue without blocking
                try:
                    jobQueue.put_nowait(job(bt_msg))
                    logging.info("{t}       bluetooth_coro() queued a job".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
                except asyncio.QueueFull:
                    logging.warn("{t}       bluetooth_coro() Job Queue Full".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # run every X ms
        await asyncio.sleep(BLUETOOTH_PERIOD)


async def lighting_coro():
    while True:
        # log the handler execution
        logging.info("{t}       Executing lighting_coro()".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # get job fifo lock
        async with jobLock:
            logging.info("{t}       lighting_coro() has job fifo lock".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
            # get a job without blocking
            try:
                job = jobQueue.get_nowait()
                # TODO - process the job
                logging.info("{t}       lighting_coro() processing a job".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

            except asyncio.QueueEmpty:
                # nothing to do
                logging.info("{t}       lighting_coro() Job Queue Empty".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # run every X ms
        await asyncio.sleep(LIGHTING_PERIOD)


async def schedule_tasks():
    tasks = []

    # create tasks
    tasks.append(asyncio.create_task(idle_coro()))
    tasks.append(asyncio.create_task(bluetooth_coro()))
    tasks.append(asyncio.create_task(lighting_coro()))

    # schedule tasks
    for task in tasks:
        await task
