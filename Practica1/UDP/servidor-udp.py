import socket
import time
import sys
import os
sys.path.append(os.path.abspath('../JuegoGato'))    # Subir a la capeta correspondiente para poder importar el gato
from gato import *

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8080  # The port used by the server
bufferSize = 1024
juego=0
k=0
seguir=True
sig1=False; sig2=False  # Variables para seguir o no jugando y verificar al ganador
tirosP1=0; tirosP2=0    # Numero de tiros que lleva cada jugador
timeIni=0; timeFin=0    # Tiempo de inicio y tiempo de fin del juego

with  socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:  # Abrir conexión
    UDPServerSocket.bind((HOST, PORT))

    print("Servidor UDP a la escucha")

    # Listen for incoming datagrams
    msgFromServer = "Bienvenido al juego de gato\nElige la dificultad del juego\n1. Principiante\n2. Avanzado"
    bytesToSend = str.encode(msgFromServer) # Codifica mensaje
    data,address = UDPServerSocket.recvfrom(bufferSize) # Detecta datos enviados por el cliente
    print("\nMensaje del cliente: "+str(data.decode()))
    UDPServerSocket.sendto(bytesToSend, address) # Manda Mensaje al cliente
    data,address = UDPServerSocket.recvfrom(bufferSize) # Detecta datos enviados por el cliente
    if int(str(data.decode()))==1:
        k=3; juego=Gato(k)      # Dif es el valor de 
    elif int(str(data.decode()))==2:
        k=5; juego=Gato(k*2)

    timeIni=time.time()
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
            if tirosP1>=k-1:      # Si el turno supera los 2, se verifica si es candidato a ganar
                sig1=juego.verifica(1,k)
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
            elif not (juego.t==0).all: # si los tiros sobrepasan los 4 turnos, o bien, se llena la matriz, acaba la partida
                msgFromServer=juego.verGato()   
                bytesToSend=str.encode(msgFromServer)
                UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje del tablero al cliente
                msgFromServer="\n\tGato!!!\n"
                bytesToSend=str.encode(msgFromServer)
                UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje de que es turno del cliente
                break

            juego.jugadaP2(k)

            tirosP2+=1          # Realizada la jugada, se suma un turno
            if tirosP2>=2:      # Si el turno supera los 2, se verifica si es candidato a ganar
                sig2=juego.verifica(-1,k)
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
    
    timeFin=time.time()
    print("\nMensaje del cliente: "+str(data.decode()))
    msgFromServer = str(timeFin-timeIni)+" seg."
    bytesToSend = str.encode(msgFromServer) # Codifica mensaje
    UDPServerSocket.sendto(bytesToSend, address) # Manda mensaje de que es turno del cliente