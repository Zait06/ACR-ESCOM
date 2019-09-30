import random as rand
import socket
import time
import sys
import os

HOST=input("Ingrese la IP del servidor: ")
PORT=int(input("Ingrese el puerto del servidor: "))

msgFromClient = "Conexion hecha"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = (HOST,PORT)
bufferSize = 1024
marca=""

# Create a UDP socket at client side

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clienteSock:
    clienteSock.connect((HOST, PORT))
    clienteSock.sendto(bytesToSend, serverAddressPort)  # Manda mensaje al servidor
    msgFromServer=clienteSock.recvfrom(bufferSize)    # Mensaje recibido del servidor
    msgRecib=msgFromServer[0].decode()   # Mensaje recibido y decodificado
    os.system ("clear") # Limpia la consola

    if msgRecib=="Espere":
        print(str(msgRecib)+"...")
        print("Se esta conectando con el jugador 1")
        while True:
            msgFromServer = clienteSock.recvfrom(bufferSize)    # Mensaje recibido del servidor
            msgRecib=msgFromServer[0].decode()
            if str(msgRecib)=="avanza":
                break
    elif not msgRecib=="Espere":
        print(msgFromServer[0].decode())                 # Imprime primer mensaje del servidor
        msgFromClient=input("\nDificultad: ")  # Elije las coordenadas el cliente
        bytesToSend = str.encode(msgFromClient) # Pone la dificultad
        clienteSock.sendto(bytesToSend, serverAddressPort)  # Envia la dificultad

    bytesToSend = str.encode("va") # Pone la dificultad
    clienteSock.sendto(bytesToSend, serverAddressPort)  # Manda mensaje al servidor

    msgFromServer = clienteSock.recvfrom(bufferSize)    # Marca recibida
    marca=msgFromServer[0].decode()   # Marca decoficada y guarda

    os.system("clear") # Limpia la consola

    while(True):
        msgFromServer = clienteSock.recvfrom(bufferSize)    # Mensaje recibido del servidor
        msgRecib=msgFromServer[0].decode()   # Mensaje recibido y decodificado
        if str(msgRecib)=="p":     # Si el mensaje recibido es p1, es turno del cliente para jugar
            msgFromClient=input("\nIngrese las coordenadas donde desea tirar: ")  # Elije las coordenadas el cliente
            bytesToSend = str.encode(msgFromClient) # Codifica las coordenadas
            clienteSock.sendto(bytesToSend, serverAddressPort)  # Envia las coordenadas
            os.system ("clear") # Limpia la consola
        elif str(msgRecib)=="Lugar ocupado":    # Si el lugar está ocupado, le avisa al cliente
            os.system ("clear")
            print(str(msgRecib)+"\n")
        elif str(msgRecib)=="wt":
            print("Espera...\nEs turno del otro jugador")
            time.sleep(1)
        elif str(msgRecib)=="exit":
            break
        else:
            os.system("clear")
            print("\nTu marca es: {}\n".format(marca))
            print(msgRecib) # Imprime el mensaje recibido
            
    msgFromServer = clienteSock.recvfrom(bufferSize)    # Mensaje recibido del servidor
    msgRecib=msgFromServer[0].decode()   # Mensaje recibido y decodificado
    print(str(msgRecib))
print("\n\t\tFin del juego Dx\n")       