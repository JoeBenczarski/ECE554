#
#   tasks.py
#

import asyncio

from datetime import datetime
import logging

from jobs import *
from sock_server import *
from light_services import *

# 1 ms definition
ONE_MS = 0.001

# task execution period
BLUETOOTH_PERIOD = 150*ONE_MS
LIGHTING_PERIOD  = 1000*ONE_MS

# Job queue
jobQueue = asyncio.Queue(10)
# Lock for job queue
jobLock = asyncio.Lock()

async def bluetooth_coro(services, loop, event):
    addr = ''
    port = 65432
    server = sock_server(addr, port)
    
    while True:
        # log the handler execution
        logging.info("{t}       Executing bluetooth_coro()".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        # blocking call to wait for incoming messages
        req = await server.get()
        # get a bluetooth message without blocking
        if req != None:
            logging.info("{t}       bluetooth_coro() received a request".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
            # set event to cancel ongoing job
            event.set()
            async with jobLock:
                logging.info("{t}       bluetooth_coro() has job fifo lock".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
                # add job to queue without blocking
                try:
                    jobQueue.put_nowait(job(req))
                    logging.info("{t}       bluetooth_coro() queued a job".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
                except asyncio.QueueFull:
                    logging.warn("{t}       bluetooth_coro() Job Queue Full".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

        # run every X ms
        await asyncio.sleep(BLUETOOTH_PERIOD)

async def lighting_coro(services, loop, event):
    while True:
        # log the handler execution
        logging.info("{t}       Executing lighting_coro()".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        # get job fifo lock
        async with jobLock:
            logging.info("{t}       lighting_coro() has job fifo lock".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
            try:
                # get a job without blocking
                job = jobQueue.get_nowait()
                # process the job in background to avoid blocking IO call
                future = loop.run_in_executor(None, job.process, services, event)
            except asyncio.QueueEmpty:
                # no job in queue
                logging.info("{t}       lighting_coro() Job Queue Empty".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
            except:
                logging.error("{t}       lighting_coro() unknown exception occurred!".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        # run every X ms
        await asyncio.sleep(LIGHTING_PERIOD)

async def schedule_tasks(loop, event):
    tasks = []
    servs = light_service()

    # create tasks
    tasks.append(asyncio.create_task(bluetooth_coro(servs, loop, event)))
    tasks.append(asyncio.create_task(lighting_coro(servs, loop, event)))

    # schedule tasks
    for task in tasks:
        await task
