#!/usr/bin/env python3

import socket
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8080  # The port used by the server
buffer_size = 1024

op=int(input("Elija el nombre de un libro:\n1. La biblia\n2. Hamlet.txt\n3. MobyDick\nOpcion:"))

if(op==1):
    lib="../libros/Bibla.txt"
elif(op==2):
    lib="../libros/hamlet.txt"
else:
    lib="../libros/MobyDick.txt"

archivo = open(lib, "r")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    # TCPClientSocket.sendall(b"Hello TCP server")
    for linea in archivo.readlines():
        bytesToSend = str.encode(str(lib)+" - "+linea)
        TCPClientSocket.sendall(bytesToSend)
        time.sleep(0.1)
    #data = TCPClientSocket.recv(buffer_size)
archivo.close()