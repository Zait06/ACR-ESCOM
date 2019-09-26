import logging
import socket
import time
import sys
import os
import threading
sys.path.append(os.path.abspath('../JuegoGato'))    # Subir a la capeta correspondiente para poder importar el gato
from gato import *

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

class Servidor():
    def __init__(self):
        self.HOST="127.0.0.1"; self.PORT=8080
        self.serveraddr = (self.HOST,self.PORT)
        self.jugA=list()
        self.listaConexiones=list()
        self.juego=0; self.k=0
        self.seguir=False; self.flag1=True; self.flag2=True
        self.sig1=False; self.sig2=False
        self.tirosP1=0; self.tirosP2=0    # Numero de tiros que lleva cada jugador
        self.timeIni=0; self.timeFin=0
        self.TCPServerSocket=0
        self.lock=threading.Lock()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.TCPServerSocket:
            self.TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.TCPServerSocket.bind(self.serveraddr)
            self.TCPServerSocket.listen(2)
            print("Servidor UDP a la escucha con direccion IP "+str(self.HOST))

            self.servirPorSiempre(self.TCPServerSocket,self.listaConexiones)

    def servirPorSiempre(self,socketTcp,listaconexiones):
        try:
            logging.debug('Esperando a los jugadores')
            while True:
                client_conn, client_addr = socketTcp.accept()
                print("Conectado a: ", client_addr)
                listaconexiones.append(client_conn)
                self.jugA.append(client_addr)
                thread_read=threading.Thread(target=self.recibir_datos,
                                             args=[client_conn, client_addr],
                                             name='Jugador-'+str(self.numJug))
                thread_read.start()
                self.gestion_conexiones(self.listaConexiones)
        except Exception as e:
            print(e)

    def gestion_conexiones(self,listaconexiones):
        for conn in listaconexiones:
            if conn.fileno() == -1:
                listaconexiones.remove(conn)

    def crearJuego(self,tam):
        if tam==1:
            self.k=3; self.juego=Gato(self.k)      # k son las dimensiones
        elif tam==2:
            self.k=5; self.juego=Gato(self.k*2)

    def recibir_datos(self,conn,addr):
        try:
            cur_thread=threading.current_thread()
            logging.debug('Iniciando')
            if self.flag1 and len(self.jugA)==1:
                self.flag1=False
                response = bytes("Bienvenido al juego de gato\nElige la dificultad del juego\n1. Principiante\n2. Avanzado", 'ascii')
                conn.sendall(response)
            else:
                response = bytes("Espere", 'ascii')
                conn.sendall(response)
                while True:
                    if self.flag2:
                        break

        except Exception as e:
            print(e)

s = Servidor()