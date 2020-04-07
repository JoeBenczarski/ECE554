import socket

class ip_server(object):

    def __init__(self, host, port, limit=1024):
        self.host = host
        self.port = port
        self.limit = limit
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = None
        self.client_addr = None
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(1)

    def connect(self):
        # wait for a client to connect
        self.client, self.client_addr = self.sock.accept()
        print('connected to {}'.format(self.client_addr))

    def disconnect(self):
        # client disconnected, now clean up
        self.client.close()
        self.client = None
        self.client_addr = None
        print("client disconnected")

    def get_req(self):
        req = None
        if self.client:
            data = self.client.recv(self.limit)
            if not data:
                # client closed the connection
                self.disconnect()
            else:
                # acknowledge the req
                self.client.send(b"ACK")
                # decode the received bytes
                req = data.decode("utf-8")
        return req
