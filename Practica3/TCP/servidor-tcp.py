import threading
import logging
import socket
import time
import sys
import os
sys.path.append(os.path.abspath('../JuegoGato'))    # Subir a la capeta correspondiente para poder importar el gato
from gato import *

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()

    def makeActive(self, name):
        self.lock.acquire()
        self.active.append(name)
        logging.debug('Ejecutando: %s', self.active)
        
    def makeInactive(self, name):
        self.lock.release()
        self.active.remove(name)
        logging.debug('Ejecutando: %s', self.active)

class Servidor():
    def __init__(self):
        self.HOST="127.0.0.1"; self.PORT=8080
        self.serveraddr=(self.HOST,self.PORT)
        self.jugA=list(); self.hilos=list();
        self.listaConexiones=list()
        self.juego=object; self.k=0;
        self.jueCreado=False; self.numJug=0;
        self.sig1=False; self.sig2=False;
        self.timeIni=0; self.timeFin=0; self.hayGanador=False
        self.marcas=list(); self.numPlay=0
        self.pool=ActivePool()
        self.sema=threading.Semaphore(1)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.TCPServerSocket:
            self.TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.TCPServerSocket.bind(self.serveraddr)
            self.TCPServerSocket.listen(10)
            os.system("clear")
            print("\nServidor UDP a la escucha con direccion IP "+str(self.HOST))

            self.esperaConexion(self.TCPServerSocket,self.listaConexiones)

    # Servicio a todos los clientes
    def esperaConexion(self,socketTcp,listaconexiones):
        try:
            i=0
            logging.debug('Esperando a los jugadores')
            while True:
                client_conn, client_addr = socketTcp.accept()
                logging.debug("Conectado a: "+str(client_addr))
                listaconexiones.append(client_conn)
                if self.numJug==0:
                    self.jugA.append(client_addr)
                    self.numJug+=1
                    productor=threading.Thread(target=self.crearJuego,
                                                args=[client_conn,client_addr],
                                                name='Productor')
                    productor.start()
                
                if self.numJug>0 and client_addr!=self.jugA[0]:
                    self.jugA.append(client_addr)
                    self.numJug+=1; i+=1
                    resto=threading.Thread(target=self.resto,
                                                args=[client_conn,client_addr,self.numJug],
                                                name='Resto-'+str(i))
                    resto.start()

                time.sleep(1)
                self.gestion_conexiones(self.listaConexiones)
        except Exception as e:
            print(e)

    # Gestion de hilos de conexion
    def gestion_conexiones(self,listaconexiones):
        for conn in listaconexiones:
            if conn.fileno() == -1:
                listaconexiones.remove(conn)

    def crearJuego(self,conn,addr):
        logging.debug("Creando juego")
        thread_read=threading.Thread(target=self.recibir_datos,
                                        args=[0,conn,addr,self.pool,self.sema],
                                        name='Jugador-1')
        self.hilos.append(thread_read)
        conn.sendall(str.encode("cho"))
        self.numPlay=int(conn.recv(1024).decode())
        logging.debug("Jugadores: "+str(self.numPlay))
        response=bytes("Bienvenido al juego de gato\n"+
                        "Elige la dificultad del juego\n"+
                        "1. Principiante\n2. Avanzado", 'ascii')
        conn.sendall(response)
        tam=conn.recv(1024)
        if tam==1:
            self.k=3; self.juego=Gato(self.k,self.numPlay)      # k son las dimensiones
        elif tam==2:
            self.k=5; self.juego=Gato(self.k*2,self.numPlay)
        self.jueCreado=True
        logging.debug("Juego creado: "+str(self.jueCreado))
        logging.debug("Tamanio: "+str(len(self.hilos))+" Juego: "+str(self.jueCreado))
        while True:
            if len(self.hilos)==self.numPlay and self.jueCreado:
                logging.debug("Hecho, creando jugadores.")
                for t in self.hilos:
                    self.marcas.append("-")
                    t.start()
                break
            time.sleep(1)
    
    def resto(self,conn,addr,num):
        logging.debug("Esperando la creacion del juego")
        thread_read=threading.Thread(target=self.recibir_datos,
                                        args=[num-1,conn,addr,self.pool,self.sema],
                                        name='Jugador-'+str(num))
        self.hilos.append(thread_read)
        conn.sendall(str.encode("Espere"))
        while True: 
            if len(self.hilos)==self.numPlay and self.jueCreado:
                conn.sendall(str.encode("gogo"))
                break
            time.sleep(1)
        logging.debug("Podemos continuar")

    def recibir_datos(self,fi,conn,addr,pool,s):
        logging.debug('Creado')
        data=conn.recv(1024)
        m=str(data.decode())
        self.marcas[fi]=m
        try:
            seguir=True
            time.sleep(1)
            while seguir:
                with s:
                    name=threading.currentThread().getName()
                    pool.makeActive(name)
                    pool.makeInactive(name)
                time.sleep(1)
            time.sleep(1)
            print("Conexion cerrada por {}".format(addr))
        except Exception as e:
            print(e)
        finally:
            self.numJug-=1; 
            conn.close()

s=Servidor()