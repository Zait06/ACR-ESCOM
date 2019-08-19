import socket
import sys
import os
sys.path.append(os.path.abspath('../JuegoGato'))    # Subir a la capeta correspondiente para poder importar el gato
from gato import *

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 54321  # The port used by the server
msgFromClient = "Conexion hecha"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = ("127.0.0.1", 54321)
bufferSize = 1024
juego=Gato()

# Create a UDP socket at client side

with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as UDPClientSocket:
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)  # Send to server using created UDP socket
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)    # Mensaje recibido del servidor
    print(msgFromServer[0].decode('utf-8'))

    while(True):
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)    # Mensaje recibido del servidor
        msgRecib=msgFromServer[0].decode('utf-8')   # Mensaje recivido
        if str(msgRecib)=="p1":     # Si el mensaje recibido es p1, es turno del cliente
            msgFromClient=juego.jugadaP1()
            bytesToSend = str.encode(msgFromClient)
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        else:
            print(msgRecib)
        