import asyncio
import concurrent.futures

from jobs import job
from light_services import light_service

import time

async def output_coro(out_queue, in_event, seconds):
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
        # process the job
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            print('output_coro() processing the job')
            future = await loop.run_in_executor(pool, currJob.process, services, in_event)
        # allow other tasks to run
        await asyncio.sleep(seconds)
