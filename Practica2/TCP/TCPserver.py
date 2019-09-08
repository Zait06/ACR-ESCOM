import socket
import time
import sys
import os
import threading
sys.path.append(os.path.abspath('../JuegoGato'))    # Subir a la capeta correspondiente para poder importar el gato
from gato import *

class Servidor():
    def __init__(self):
        self.HOST="127.0.0.1"; self.PORT=8080
        self.serveraddr = (self.HOST,self.PORT)
        self.jugA=list()
        self.listaConexiones=list()
        self.juego=0; self.k=0
        self.seguir=False
        self.sig1=False; self.sig2=False
        self.tirosP1=0; self.tirosP2=0    # Numero de tiros que lleva cada jugador
        self.timeIni=0; self.timeFin=0
        self.TCPServerSocket=0

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.TCPServerSocket:
            self.TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.TCPServerSocket.bind(self.serveraddr)
            self.TCPServerSocket.listen(2)
            print("Servidor UDP a la escucha con direccion IP "+str(self.HOST))

            self.servirPorSiempre(self.TCPServerSocket,self.listaConexiones)

    def servirPorSiempre(self,socketTcp,listaconexiones):
        try:
            while True:
                client_conn, client_addr = socketTcp.accept()
                print("Conectado a: ", client_addr)
                listaconexiones.append(client_conn)
                self.jugA.append(client_addr)
                thread_read = threading.Thread(target=self.recibir_datos, args=[client_conn, client_addr])
                thread_read.start()
                self.gestion_conexiones(self.listaConexiones)
        except Exception as e:
            print(e)

    def gestion_conexiones(self,listaconexiones):
        for conn in listaconexiones:
            if conn.fileno() == -1:
                listaconexiones.remove(conn)

    def otrosMensajes(self,data,tipo,conn):
        self.seguir=self.juego.jugadorPlayer(data,tipo) # Verficar lugar ocupado
        time.sleep(6)
        response=bytes(self.juego.verGato(),'ascii')
        conn.sendall(response)


    def crearJuego(self,tam):
        if tam==1:
            self.k=3; self.juego=Gato(self.k)      # k son las dimensiones
        elif tam==2:
            self.k=5; self.juego=Gato(self.k*2)

    def recibir_datos(self,conn,addr):
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
                    if addr==self.jugA[1]:
                        response = bytes("O", 'ascii')
                        conn.sendall(response)
                    else:
                        response = bytes("X", 'ascii')
                        conn.sendall(response)
                        self.crearJuego(int(str(data.decode())))
                    
                    time.sleep(3)
                    self.timeIni=time.time()
                    self.seguir=True
                    
                    if addr==self.jugA[0]:
                        response=bytes(self.juego.verGato(),'ascii')
                        conn.sendall(response)
                        time.sleep(0.5)
                        msgFromServer='p1'
                        bytesToSend=str.encode(msgFromServer)
                        conn.sendall(bytesToSend) # Manda mensaje al cliente
                    else:
                        response=bytes(self.juego.verGato(),'ascii')
                        conn.sendall(response)
                        time.sleep(0.5)
                        time.sleep(5)
                        msgFromServer='p1'
                        bytesToSend=str.encode(msgFromServer)
                        conn.sendall(bytesToSend) # Manda mensaje al cliente
                elif self.seguir and data:
                    if addr==self.jugA[0]:
                        self.otrosMensajes(str(data.decode()),1,conn)
                        time.sleep(3)
                    else:
                        time.sleep(3)
                        self.otrosMensajes(str(data.decode()),-1,conn)
                    time.sleep(0.5)
                    msgFromServer='p1'
                    bytesToSend=str.encode(msgFromServer)
                    conn.sendall(bytesToSend) # Manda mensaje al cliente

                if not data:
                    print("Conexion cerrada por {}".format(addr))
                    self.timeFin=time.time()
                    break
        except Exception as e:
            print(e)
        finally:
            conn.close()

s = Servidor()