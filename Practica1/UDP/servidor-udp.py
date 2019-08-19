import socket
import sys
import os
sys.path.append(os.path.abspath('../JuegoGato'))    # Subir a la capeta correspondiente para poder importar el gato
from gato import *

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 54321  # The port used by the server
bufferSize = 1024
juego=Gato()
# msgFromServer = "Hello UDP Client"          # Mensaje a mandar
# bytesToSend = str.encode(msgFromServer)     # Mensaje pasado a bits

with  socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:  # Abrir conexión
    UDPServerSocket.bind((HOST, PORT))

    print("Servidor UDP a la escucha")

    # Listen for incoming datagrams
    msgFromServer = "Bienvenido al juego de gato\n"
    bytesToSend = str.encode(msgFromServer)
    data,address = UDPServerSocket.recvfrom(bufferSize) # Detecta datos enviados por el cliente
    UDPServerSocket.sendto(bytesToSend, address) # Manda Mensaje al cliete

    while (True):
        print("\nMensaje del cliente: "+str(data.decode()))
        msgFromServer=juego.verGato()
        bytesToSend=str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje al cliente

        msgFromServer='p1'
        bytesToSend=str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje al cliente

        data,address = UDPServerSocket.recvfrom(bufferSize) # Detecta datos enviados por el cliente
        juego.ocupado(str(data.decode()),1) # Verficar lugar ocupado