import socket
import sys
import os

HOST=input("Ingrese la IP del servidor: ")
PORT=int(input("Ingrese el puerto del servidor: "))

msgFromClient = "Conexion hecha"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = (HOST,PORT)
bufferSize = 1024


# Create a UDP socket at client side

with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as UDPClientSocket:
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)  # Manda mensaje al servidor
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)    # Mensaje recibido del servidor
    os.system ("clear") # Limpia la consola
    print(msgFromServer[0].decode())                 # Imprime primer mensaje del servidor
    msgFromClient=input("\nDificultad: ")  # Elije las coordenadas el cliente
    bytesToSend = str.encode(msgFromClient) # Pone la dificultad
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)  # Envia las coordenadas
    os.system ("clear") # Limpia la consola

    while(True):
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)    # Mensaje recibido del servidor
        msgRecib=msgFromServer[0].decode()   # Mensaje recibido y decodificado
        if str(msgRecib)=="p1":     # Si el mensaje recibido es p1, es turno del cliente para jugar
            msgFromClient=input("\nIngrese las coordenadas donde desea tirar: ")  # Elije las coordenadas el cliente
            bytesToSend = str.encode(msgFromClient) # Codifica las coordenadas
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)  # Envia las coordenadas
            os.system ("clear") # Limpia la consola
        elif str(msgRecib)=="Lugar ocupado":    # Si el lugar está ocupado, le avisa al cliente
            os.system ("clear")
            print(msgRecib)
        elif str(msgRecib)=="exit":
            break
        else:
            print(msgRecib) # Imprime el mensaje recibido

print("\t\tFin del juego Dx\n")       