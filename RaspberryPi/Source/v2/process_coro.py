import asyncio

from jobs import job

async def process_coro(in_queue, out_queue, seconds):
    print('process_coro() started')
    while True:
        print('process_coro() running')
        # wait for the input queue
        msg = await in_queue.get()
        print('process_coro() got message from queue')
        # create job from the message
        newJob = job(msg)
        # put job in the output queue
        await out_queue.put(newJob)
        print('process_coro() put job in queue: {}'.format(newJob.cmd))
        # allow other tasks to run
        await asyncio.sleep(seconds)
