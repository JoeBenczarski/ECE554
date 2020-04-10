import bluetooth

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.bind(("", 1))
sock.listen(1)
conn, addr = sock.accept()
print("Accepted connection from {}".format(addr))
data = conn.recv(1024)
conn.send(b"ACK")
req = data.decode("utf-8")        
print(req)
conn.close()
sock.close()