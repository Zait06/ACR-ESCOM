#!/usr/bin/env python3
import socket
import time
import sys
import os
import threading
sys.path.append(os.path.abspath('../JuegoGato'))    # Subir a la capeta correspondiente para poder importar el gato
from gato import *

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8080  # The port used by the server
bufferSize = 1024
juego=Gato(3)
k=0
flag=False
seguir=True
sig1=False; sig2=False  # Variables para seguir o no jugando y verificar al ganador
tirosP1=0; tirosP2=0    # Numero de tiros que lleva cada jugador
timeIni=0; timeFin=0    # Tiempo de inicio y tiempo de fin del juego
jugA=list()
listaConexiones=list()

def crearJuego(tam):
    if tam==1:
        k=3; juego=Gato(k)      # k son las dimensiones
    elif tam==2:
        k=5; juego=Gato(k*2)

def servirPorSiempre(socketTcp, listaconexiones):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a: ", client_addr)
            listaconexiones.append(client_conn)
            jugA.append(client_addr)
            thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr])
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)


def recibir_datos(conn, addr):
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
        while True:
            data = conn.recv(1024)
            print("{} - {}".format(addr, data))
            if str(data.decode())=="Conexion hecha":
                response = bytes("Bienvenido al juego de gato\nElige la dificultad del juego\n1. Principiante\n2. Avanzado", 'ascii')
                conn.sendall(response)
           
            if str(data.decode())=="1" or str(data.decode())=="2":
                if addr==jugA[1]:
                    response = bytes("O", 'ascii')
                    conn.sendall(response)
                else:
                    response = bytes("X", 'ascii')
                    conn.sendall(response)
                    crearJuego(int(str(data.decode())))

                timeIni=time.time()
                response=bytes(juego.verGato(),'ascii')
                conn.sendall(response)
            else:
                pass

            if not data:
                print("Conexion cerrada por {}".format(addr))
                break
    except Exception as e:
        print(e)
    finally:
        conn.close()



listaConexiones = []

serveraddr = (HOST,PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(2)
    print("Servidor UDP a la escucha con direccion IP "+str(HOST))

    servirPorSiempre(TCPServerSocket, listaConexiones)