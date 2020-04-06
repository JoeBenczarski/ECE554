import asyncio
import concurrent.futures

from server import ip_server
#from bt_server import bt_server

async def input_coro(in_queue, in_event, seconds):
    print('input_coro() started')
    loop = asyncio.get_running_loop()
    sock = ip_server('', 65432)
    while True:
        print('input_coro() running')

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            # check for existing connection
            if not sock.client:
                # wait for connection from client
                await loop.run_in_executor(pool, sock.connect)
            # wait for a request
            req = await loop.run_in_executor(pool, sock.get_req)
        # put request in queue
        await in_queue.put(req)
        print('input_coro() put request in queue')
        # set event for new input
        in_event.set()
        # allow other tasks to run
        await asyncio.sleep(seconds)
