import asyncio
import concurrent.futures

#from ip_server import ip_server
from bluetooth import *
from bt_server import bt_server

async def input_coro(in_queue, in_event, seconds):
    print('input_coro() started')
    loop = asyncio.get_running_loop()
    sock = bt_server("", PORT_ANY)
    while True:
        print('input_coro() running')
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            # check for existing connection
            if sock.client is None:
                # wait for connection from client
                print('input_coro() waiting for connection')
                await loop.run_in_executor(pool, sock.connect)
            # wait for a request
            print('input_coro() waiting for request')
            req = await loop.run_in_executor(pool, sock.get_req)
        # put request in queue
        await in_queue.put(req)
        print('input_coro() queued request: {}'.format(req))
        # set event for new input
        in_event.set()
        # allow other tasks to run
        await asyncio.sleep(seconds)
