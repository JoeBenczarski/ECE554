import asyncio
import socket

class server(object):
    
    def __init__(self, host, port, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=-1, limit=1024):
        self.host = host
        self.port = port
        self.family = family
        self.type = type
        self.proto = proto
        self.limit = limit
        self.sock = socket.socket(family, type, proto)
        self.sock.bind((host, port))
        self.sock.listen()

    def get(self):
        chunks = []            
        conn, addr = self.sock.accept()
        print('connected to {}'.format(addr))
        with conn:
            while True:
                chunk = conn.recv(self.limit)
                if not chunk:
                    break
                chunks.append(chunk.decode("utf-8"))
                #conn.sendall(b'ACK')
        req = ''.join(chunks)
        return req
