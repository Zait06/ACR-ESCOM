import threading
import logging
import socket
import time
import sys
import os
sys.path.append(os.path.abspath('../JuegoGato'))    # Subir a la capeta correspondiente para poder importar el gato
from gato import *

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

class Servidor():
    def __init__(self):
        self.HOST="127.0.0.1"; self.PORT=8080
        self.serveraddr=(self.HOST,self.PORT)
        self.jugA=list(); self.hilos=list();
        self.listaConexiones=list()
        self.juego=object; self.k=0; self.bandera=True
        self.jueCreado=False; self.numJug=0
        self.flag1=True; self.flag2=False; self.flag3=True
        self.sig1=False; self.sig2=False; self.jeje=True
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
        self.jueCreado=True
    
    def tipoMarca(self,addr):
        ese=0
        if addr==self.jugA[0]:
            ese=1
        else:
            ese=-1
        return ese

    def mandarTurno(self,conn):
        conn.sendall(str.encode("play"))

    def mandarTablero(self,conn,addr):
        tablero=self.juego.verGato()
        response=str.encode(str(tablero))
        conn.sendall(response)

    # Marca del jugador y primer tiro
    def mandarMarca(self,conn,addr):
        self.timeIni=time.time()
        logging.debug("Mandando marca y tablero")
        if addr==self.jugA[1] and not self.sig2:
            response=bytes("O", 'ascii')
            conn.sendall(response)
            self.mandarTablero(conn,addr)
            time.sleep(2)
            conn.sendall(bytes("wt", 'ascii'))
            self.sig2=self.esperoYo(self.candado,self.sig2)
        else:
            self.juegoYo(self.candado,conn)
            response=bytes("X", 'ascii')
            conn.sendall(response)
            self.mandarTablero(conn,addr)
            time.sleep(2)
            self.mandarTurno(conn)
            time.sleep(2)
        logging.debug("Marca y tablero enviadas")
        time.sleep(1)

    def juegoYo(self,lock,conn):
        logging.debug('Candado iniciando')
        lock.acquire()
        logging.debug('Candado ocupado')
        time.sleep(1)
    
    def libera(self,lock):
        if not self.bandera:
            logging.debug('Candado disponible')
            lock.release()

    def esperoYo(self,lock,tur):
        logging.debug('Espera inicianda')
        flag=True
        while flag:
            time.sleep(0.5)
            have_it = lock.acquire(0)
            try:
                if have_it:
                    flag=False; tur=True
                    logging.debug('Candado obtenido')
            finally:
                if have_it:
                    logging.debug('Esperando tiro')
                    lock.release()
        return tur

    def recibir_datos(self,conn,addr):
        conteo=0;
        try:
            logging.debug('Jugador iniciando')
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
                elif conteo>2 and self.jeje:
                    self.bandera=False
                    if addr==self.jugA[0]:
                        self.libera(self.candado)
                        self.sig2=True; self.jeje=False
                    elif addr==self.jugA[1]:
                        self.libera(self.candado)
                    
                if len(self.jugA)>1:
                    if not self.flag1 and addr==self.jugA[1] and self.flag3:  # Si es el jugador 2, manda señal de espera
                        response = bytes("Espere", 'ascii')
                        conn.sendall(response)
                        while True:
                            if self.flag2:
                                conn.sendall(bytes("avanza",'ascii'))
                                break
                            time.sleep(1)
                        logging.debug('Podemos continuar')
                        self.flag3=False

                if self.jueCreado:
                    if self.sig1 or self.sig2:
                        self.juego.jugadorPlay(str(data.decode()),self.tipoMarca(addr))
                        self.mandarTablero(conn,addr)
                        logging.debug("Tablero enviado")
                        time.sleep(2)
                        if not self.sig1 and self.sig2:
                            if addr==self.jugA[1]:
                                self.juegoYo(self.candado,conn)
                                self.mandarTurno(conn)
                            else:
                                conn.sendall(bytes("wt", 'ascii'))
                                self.sig1=self.esperoYo(self.candado,self.sig1)
                    final1=self.juego.verifica(1,self.k)
                    final2=self.juego.verifica(-1,self.k)
                    if final1 and conteo>2:
                        logging.debug("Ganador jugador 1")
                        break
                    elif final2 and conteo>2:
                        logging.debug("Ganador jugador 2")
                        break
                    elif self.juego.empate() and conteo>2:
                        logging.debug("Empate")
                        break
                
                conteo+=1
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