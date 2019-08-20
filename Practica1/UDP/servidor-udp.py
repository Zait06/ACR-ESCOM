import socket
import sys
import os
sys.path.append(os.path.abspath('../JuegoGato'))    # Subir a la capeta correspondiente para poder importar el gato
from gato import *

HOST = "10.100.66.254"  # The server's hostname or IP address
PORT = 8080  # The port used by the server
bufferSize = 1024
seguir=True
juego=Gato()
sig1=False; sig2=False  # Variables para seguir o no jugando y verificar al ganador
tirosP1=0; tirosP2=0    # Numero de tiros que lleva cada jugador

with  socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:  # Abrir conexión
    UDPServerSocket.bind((HOST, PORT))

    print("Servidor UDP a la escucha")

    # Listen for incoming datagrams
    msgFromServer = "Bienvenido al juego de gato\n"
    bytesToSend = str.encode(msgFromServer)
    data,address = UDPServerSocket.recvfrom(bufferSize) # Detecta datos enviados por el cliente
    UDPServerSocket.sendto(bytesToSend, address) # Manda Mensaje al cliente

    while (True):
        print("\nMensaje del cliente: "+str(data.decode()))
        msgFromServer=juego.verGato()
        bytesToSend=str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje al cliente

        msgFromServer='p1'
        bytesToSend=str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje al cliente

        data,address = UDPServerSocket.recvfrom(bufferSize) # Detecta datos enviados por el cliente
        
        seguir=juego.ocupado(str(data.decode()),1) # Verficar lugar ocupado

        if seguir:

            tirosP1+=1          # Realizada la jugada, se suma un turno
            if tirosP1>=2:      # Si el turno supera los 2, se verifica si es candidato a ganar
                sig1=juego.verifica(1)
            if sig1:            # Si es verdadero, acaba el juego y el ganador es el jugador 1
                msgFromServer=juego.verGato()   
                bytesToSend=str.encode(msgFromServer)
                UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje del tablero al cliente
                msgFromServer="\n\tEl ganador es el jugador 1!!!\n"
                bytesToSend=str.encode(msgFromServer)
                UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje de que ha ganado
                msgFromServer="exit"
                bytesToSend=str.encode(msgFromServer)
                UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje de la conexión se cierrar
                break
            elif tirosP1>=4 and tirosP2>=4: # si los tiros sobrepasan los 4 turnos, o bien, se llena la matriz, acaba la partida
                msgFromServer=juego.verGato()   
                bytesToSend=str.encode(msgFromServer)
                UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje del tablero al cliente
                msgFromServer="\n\tGato!!!\n"
                bytesToSend=str.encode(msgFromServer)
                UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje de que es turno del cliente
                break

            juego.jugadaP2()

            tirosP2+=1          # Realizada la jugada, se suma un turno
            if tirosP2>=2:      # Si el turno supera los 2, se verifica si es candidato a ganar
                sig2=juego.verifica(-1)
            if sig2:            # Si es verdadero, acaba el juego y el ganador es el jugador 2
                msgFromServer=juego.verGato()   
                bytesToSend=str.encode(msgFromServer)
                UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje del tablero al cliente
                msgFromServer="\n\tEl ganador es el jugador 2!!!\n"
                bytesToSend=str.encode(msgFromServer)
                UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje de que ha ganado el servidor
                msgFromServer="exit"
                bytesToSend=str.encode(msgFromServer)
                UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje de la conexión se cierrar
                break
        else:
            msgFromServer='Lugar ocupado'
            bytesToSend=str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje del lugar ocupado al cliente