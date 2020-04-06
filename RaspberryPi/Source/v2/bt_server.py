import bluetooth

class bt_server(object):

    def __init__(self, host, port, limit=1024):
        self.host = host
        self.port = port
        self.limit = limit
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client = None
        self.client_addr = None
        self.sock.bind((host, port))
        self.sock.listen(1)

    def connect(self):
        self.client, self.client_addr = self.sock.accept()
        print('connected to {}'.format(addr))

    def get_req(self):
        req = None
        if self.client:
            with self.client:
                data = conn.recv(self.limit)
                self.client.send("ACK")
                req = data.decode("utf-8")
        return req
