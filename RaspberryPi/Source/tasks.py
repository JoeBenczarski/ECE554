#
#   tasks.py
#


import asyncio
import logging
from datetime import datetime
from Source.bluetooth import bluetooth

# 1 ms definition
ONE_MS = 0.001

# task execution period
IDLE_PERIOD      = 10*ONE_MS
BLUETOOTH_PERIOD = 100*ONE_MS
LIGHTING_PERIOD  = 150*ONE_MS

# lock for job access
job_lock = asyncio.Lock()


async def idle_coro():
    while True:
        # log the handler execution
        #logging.info("{t}       Executing idle_coro()".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # run every X ms
        await asyncio.sleep(IDLE_PERIOD)


async def bluetooth_coro(bt, jobs):
    while True:
        # log the handler execution
        logging.info("{t}       Executing bluetooth_coro()".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # check for incoming bluetooth messages without blocking
        bt.check_nowait()

        # get job fifo lock
        async with job_lock:
            logging.info("{t}       bluetooth_coro() has job fifo lock".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
            # get a bluetooth message without blocking
            if bt.last_msg != None:
                # add job to queue without blocking
                try:
                    jobs.put_nowait(bt.last_msg)
                except asyncio.QueueFull:
                    logging.warn("{t}       bluetooth_coro() Job Queue Full".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # run every X ms
        await asyncio.sleep(BLUETOOTH_PERIOD)


async def lighting_coro(jobs):
    while True:
        # log the handler execution
        logging.info("{t}       Executing lighting_coro()".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # get job fifo lock
        async with job_lock:
            logging.info("{t}       lighting_coro() has job fifo lock".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
            # get a job without blocking
            try:
                job = jobs.get_nowait()
                # TODO - process the job
                pass
            except asyncio.QueueEmpty:
                # nothing to do
                logging.info("{t}       lighting_coro() Job Queue Empty".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # run every X ms
        await asyncio.sleep(LIGHTING_PERIOD)


async def schedule_tasks():
    tasks = []
    bt = bluetooth()
    jobs = asyncio.Queue(10)

    # create tasks
    tasks.append(asyncio.create_task(idle_coro()))
    tasks.append(asyncio.create_task(bluetooth_coro(bt, jobs)))
    tasks.append(asyncio.create_task(lighting_coro(jobs)))

    # schedule tasks
    for task in tasks:
        await task
