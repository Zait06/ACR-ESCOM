import random as rand
import socket
import time
import sys
import os

os.system("clear")
HOST=input("\nIngrese la IP del servidor: ")
PORT=int(input("Ingrese el puerto del servidor: "))

serverAddressPort = (HOST,PORT)
bufferSize = 1024
marca=""

# Create a UDP socket at client side

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clienteSock:
    clienteSock.connect((HOST, PORT))
    msgFromServer=clienteSock.recvfrom(bufferSize)    # Mensaje recibido del servidor
    msgRecib=msgFromServer[0].decode()   # Mensaje recibido y decodificado
    os.system ("clear") # Limpia la consola

    if msgRecib=="Espere":
        print(str(msgRecib)+"...")
        print("Se estan contectando todos los jugadores")
        msgFromServer = clienteSock.recvfrom(bufferSize)    # Mensaje recibido del servidor
        msgRecib=msgFromServer[0].decode()
        if str(msgRecib)=="gogo":
            time.sleep(2)
    elif msgRecib=="cho":
        msgFromClient=input("\nNumero de jugadores: ")  # Elije las coordenadas el cliente
        bytesToSend = str.encode(msgFromClient) # Da el numero de jugadores
        clienteSock.sendto(bytesToSend, serverAddressPort)  # Envia el numero de jugadores
        os.system ("clear") # limpia consola
        msgFromServer = clienteSock.recvfrom(bufferSize)    # Mensaje recibido del servidor
        msgRecib=msgFromServer[0].decode()   # Mensaje decodificado
        print(msgRecib)
        msgFromClient=input("\nDificultad: ")  # Pone la dificultad
        bytesToSend = str.encode(msgFromClient) # Codifica dificultad
        clienteSock.sendto(bytesToSend, serverAddressPort)  # Envia la dificultad

    os.system("clear") # Limpia la consola

    marca=input("Ingrese una marca para identificarse: ")
    bytesToSend = str.encode(marca) # Codifica dificultad
    clienteSock.sendto(bytesToSend, serverAddressPort)  # Envia la dificultad

    os.system("clear") # Limpia la consola

    while(True):
        msgFromServer = clienteSock.recvfrom(bufferSize)    # Mensaje recibido del servidor
        msgRecib=msgFromServer[0].decode()   # Mensaje recibido y decodificado
        if str(msgRecib)=="play":     # Si el mensaje recibido es p1, es turno del cliente para jugar
            msgFromClient=input("Su turno.\nIngrese las coordenadas donde desea tirar: ")  # Elije las coordenadas el cliente
            bytesToSend = str.encode(msgFromClient) # Codifica las coordenadas
            clienteSock.sendto(bytesToSend, serverAddressPort)  # Envia las coordenadas
        elif str(msgRecib)=="Lugar ocupado":    # Si el lugar está ocupado, le avisa al cliente
            os.system ("clear")
            print(str(msgRecib)+"\n")
        elif str(msgRecib)=="wt":
            print("Espera...\nEs turno de otro jugador")
            time.sleep(1)
        elif str(msgRecib)=="exit":
            break
        else:
            os.system("clear")
            print("\nTu marca es: {}\n".format(marca))
            print(msgRecib) # Imprime el mensaje recibido
            time.sleep(1.5)
            
    msgFromServer = clienteSock.recvfrom(bufferSize)    # Mensaje recibido del servidor
    msgRecib=msgFromServer[0].decode()   # Mensaje recibido y decodificado
    print(str(msgRecib))
print("\n\t\tFin del juego Dx\n")       