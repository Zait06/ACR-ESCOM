#!/usr/bin/env python3

import socket
import time
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))  # Dirección y puertos para la comunicación
    TCPServerSocket.listen()    # Servidor a la escucha
    print("Esperando la llamada del cliente (LISTEN)")
    print("El servidor TCP esta disponible y en espera de solicitudes")

    print("Revisa si el LISTEN ha sido ejecutaedo")
    Client_conn, Client_addr = TCPServerSocket.accept()
    print("Acepta al cliete y lo conecta y manda el ACK=1")
    with Client_conn:
        print("Conectado a", Client_addr)
        while True:
            print("Esperando a recibir datos... ")
            data = Client_conn.recv(buffer_size)
            print("(SYN RCVD)")
            print ("Recibido,", data,"   de ", Client_addr)
            if not data:
                break
            print("(ESTABLISHED)")
            print("Enviando respuesta a", Client_addr)
            print("Bandera FIN recibida para acabar la comunicacion")
            print("Manda ACK y FIN para cerrar la conexion (FIN WAIT 2)")
            Client_conn.sendall(data)
            print("(CLOSE WAIT)")
        print("Se cierra la conexion (CLOSING)")

