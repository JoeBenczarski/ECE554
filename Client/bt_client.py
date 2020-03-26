"""
A simple Python script to send messages to a sever over Bluetooth using
Python sockets (with Python 3.3 or above).
"""

import socket

serverMACAddress = '9c:b6:d0:c3:26:e8'
port = 3

with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as s:
	s.connect((serverMACAddress, port))
	s.sendall(b'ON 255 255 255')
	data = s.recv(1024)
	
print('Received', repr(data))
