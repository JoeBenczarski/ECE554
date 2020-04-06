import asyncio
import concurrent.futures

from jobs import job
from light_services import light_service

import time

def blocking_io(event):
    print("blocking_io started")
    i = 0
    while not event.is_set():
        print("blocking_io running: {}".format(i))
        time.sleep(1)
        i += 1
    print("blocking_io cancelled")
    return True

async def output_coro(out_queue, in_event):
    print('output_coro() started')
    loop = asyncio.get_running_loop()
    services = light_service()
    while True:
        print('output_coro() running')
        # get a job
        currJob = await out_queue.get()
        print('output_coro() got from queue: {}'.format(currJob.cmd))
        # clear input event
        in_event.clear()
        # run job processing in another thread
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = await loop.run_in_executor(pool, currJob.process, services, in_event)
        # allow other tasks to run
        await asyncio.sleep(0.250)
