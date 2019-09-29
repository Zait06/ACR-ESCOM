import logging
import socket
import time
import sys
import os
import threading
sys.path.append(os.path.abspath('../JuegoGato'))    # Subir a la capeta correspondiente para poder importar el gato
from gato import *

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

class Servidor():
    def __init__(self):
        self.HOST="127.0.0.1"; self.PORT=8080
        self.serveraddr = (self.HOST,self.PORT)
        self.jugA=list(); self.hilos=list();
        self.listaConexiones=list()
        self.juego=object; self.k=0
        self.seguir=False; self.numJug=0
        self.flag1=True; self.flag2=False; self.flag3=True
        self.sig1=False; self.sig2=False
        self.tirosP1=0; self.tirosP2=0    # Numero de tiros que lleva cada jugador
        self.timeIni=0; self.timeFin=0
        self.candado=threading.Lock()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.TCPServerSocket:
            self.TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.TCPServerSocket.bind(self.serveraddr)
            self.TCPServerSocket.listen(2)
            print("Servidor UDP a la escucha con direccion IP "+str(self.HOST))

            self.servirPorSiempre(self.TCPServerSocket,self.listaConexiones)

    # Servicio a todos los clientes
    def servirPorSiempre(self,socketTcp,listaconexiones):
        try:
            logging.debug('Esperando a los jugadores')
            while True:
                client_conn, client_addr = socketTcp.accept()
                print("Conectado a: ", client_addr)
                listaconexiones.append(client_conn)
                self.jugA.append(client_addr)
                self.numJug+=1
                thread_read=threading.Thread(target=self.recibir_datos,
                                             args=[client_conn, client_addr],
                                             name='Jugador-'+str(self.numJug))
                self.hilos.append(thread_read)
                thread_read.start()
                self.gestion_conexiones(self.listaConexiones)
        except Exception as e:
            print(e)

    # Gestion de hilos de conexion
    def gestion_conexiones(self,listaconexiones):
        for conn in listaconexiones:
            if conn.fileno() == -1:
                listaconexiones.remove(conn)

    # Creacion de juego
    def crearJuego(self,tam):
        if tam==1:
            self.k=3; self.juego=Gato(self.k)      # k son las dimensiones
        elif tam==2:
            self.k=5; self.juego=Gato(self.k*2)
    
    # Marca del jugador
    def mandarMarca(self,conn,addr):
        bandera=False
        logging.debug("Mandando marca")
        if addr==self.jugA[1] and not self.sig2:
            response=bytes("O", 'ascii')
            bandera=True
        else:
            response=bytes("X", 'ascii')
        conn.sendall(response)
        logging.debug("Marca enviada")
        time.sleep(2)

    def iniJuego(self,conn,addr):
        tablero=self.juego.verGato()
        response=str.encode(str(tablero))
        conn.sendall(response)
        if self.jugA[1]==addr:
            conn.sendall(str.encode("wt"))
            time.sleep(3)
            tablero=self.juego.verGato()
            response=str.encode(str(tablero))
            conn.sendall(response)
        else:
            conn.sendall(str.encode("p"))
        self.sig1=False; self.sig2=True

    def juegoYo(self,lock):
        logging.debug('Iniciando')
        lock.acquire()
        try:
            logging.debug('Ocupado')
        finally:
            logging.debug('Disponible')
            lock.release()
        time.sleep(1)

    def esperoYo(self,lock,hi):
        logging.debug('Iniciando')
        bandera=True
        while bandera:
            time.sleep(0.5)
            have_it = lock.acquire(0)
            try:
                if have_it:
                    bandera=False; hi=True
            finally:
                if have_it:
                    lock.release()
        return hi

    def recibir_datos(self,conn,addr):
        try:
            logging.debug('Iniciando')
            while True:
                data=conn.recv(1024)
                print("{} - {}".format(addr, data))
                if self.flag1 and len(self.jugA)==1:    # Si es el jugador dos, mandará el mensaje
                    self.flag1=False;
                    response = bytes("Bienvenido al juego de gato\n"+
                                        "Elige la dificultad del juego\n"+
                                        "1. Principiante\n2. Avanzado", 'ascii')
                    conn.sendall(response)
                elif str(data.decode())=="1" or str(data.decode())=="2":    # Creación del juego
                    self.flag2=True
                    self.crearJuego(int(data.decode()))
                elif str(data.decode())=="va":
                    self.mandarMarca(conn,addr) # Mandar Marca
                    self.iniJuego(conn,addr) # Primera jugada
                elif not self.flag1 and addr==self.jugA[1] and self.flag3:  # Si es el jugador 2 manda señal de espera
                    response = bytes("Espere", 'ascii')
                    conn.sendall(response)
                    while True:
                        if self.flag2:
                            conn.sendall(bytes("avanza",'ascii'))
                            break
                        time.sleep(1)
                    logging.debug('Podemos continuar')
                    self.flag3=False

                final1=self.juego.verifica(1,self.k)
                final2=self.juego.verifica(-1,self.k)
                if final1:
                    logging.debug("Ganador jugador 1")
                    break
                elif final2:
                    logging.debug("Ganador jugador 2")
                    break
                elif self.juego.empate():
                    logging.debug("Empate")
                    break
                
                if not data:
                    print("Conexion cerrada por {}".format(addr))
                    self.timeFin=time.time()
                    break 
        except Exception as e:
            print(e)
        finally:
            self.numJug-=1
            conn.close()

s = Servidor()  # Ejecucion del servidor