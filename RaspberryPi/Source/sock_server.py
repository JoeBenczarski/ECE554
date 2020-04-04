#
#   sock_server.py
#

import asyncio
from datetime import datetime
import logging
import socket
import bluetooth

class sock_server(object):
    """class to abstract socket server functionality"""
    def __init__(self, address, port, family=socket.AF_INET, type=socket.SOCK_STREAM, protocol=-1):
        self.addr = address
        self.port = port
        self.family = family
        self.type = type
        self.protocol = protocol
        logging.info("{t}       sock_server created".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))

    async def get(self):
        """coroutine function to receive data over socket"""
        data = []
        loop = asyncio.get_running_loop()
        # log start of execution
        logging.info("{t}       sock_server::get() started".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]))
        # create socket
        
        # IP based socket
        with socket.socket(self.family, self.type, self.protocol) as sock:
            sock.bind((self.addr, self.port))       # bind to specific address and port
            sock.listen()                           # enable server to accept connections
            conn, addr = await loop.run_in_executor(None, sock.accept)
            with conn:
                # connected by addr
                logging.info("{t}       sock_server::get() connected to {a}".format(t=datetime.utcnow().strftime('%H:%M:%S.%f')[:-3], a=addr))
                while True:                         # loop over all blocking read calls
                    bytes = conn.recv(1024)         # block to read data from client
                    if not bytes:                   # data empty when client closes connection
                        break
                    conn.sendall(bytes)             # echo data back to client
                    data.append(bytes.decode("utf-8"))
        
        # BT based socket
        #with bluetooth.BluetoothSocket(bluetooth.RFCOMM) as s:
        #    s.setblocking(True)
        #    s.bind((self.addr, self.port))
        #    s.listen()
        #    conn, addr = await loop.run_in_executor(None, s.accept())
        #    with conn:
        #        while True:
        #            bytes = conn.recv(1024)
        #            if not bytes:
        #                break
        #            data.append(bytes.decode("utf-8"))

        # return all the data
        msg = ''.join(data)
        return msg
