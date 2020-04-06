import asyncio

from input_coro import input_coro
from process_coro import process_coro
from output_coro import output_coro

async def schedule_tasks():
    # input event
    inEvent = asyncio.Event()
    # input queue
    inQueue = asyncio.Queue(5)
    # output job queue
    outQueue = asyncio.Queue(5)

    # schedule all coroutines as concurrent tasks
    await asyncio.gather(
        input_coro(inQueue, inEvent, 0.500),
        process_coro(inQueue, outQueue, 0.010),
        output_coro(outQueue, inEvent, 0.250)
    )
