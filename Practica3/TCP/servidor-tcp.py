"""
    Hernández López Ángel Zait
    Servidor TCP
"""
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

    def makeActive(self,name,conn,fi,juego):    # Obtencion del candado
        self.lock.acquire()
        self.active.append(name)
        logging.debug('Ejecutando')
        conn.sendall(str.encode("play"))
        dato=conn.recv(1024)    # Coordenadas del tiro
        logging.debug(str(dato.decode()))
        juego.jugadorPlay(str(dato.decode()),fi)
        
    def makeInactive(self,name,fi,juego,k):     # Verificacion y liberacion del juego
        self.active.remove(name)
        logging.debug('Liberando candado')
        acabado=juego.verifica(fi,k)
        if not acabado:
            self.libera()
        return acabado,name

    def libera(self):   # Liberacion del candado
        self.lock.release()

class Servidor():
    def __init__(self):
        self.HOST="192.168.1.66"; self.PORT=8080    # Direccion y puerto del servidor
        self.serveraddr=(self.HOST,self.PORT)   # Conexion de IP
        self.jugA=list(); self.hilos=list()     # Listas de direccion e hilos de los jugadores
        self.listaConexiones=list()     # Lista de conexiones de los jugadores
        self.juego=object; self.k=0; self.fin=False # juego=JuegoGato; k=tamaño de la linea; fin=Si se acabo el juego
        self.jueCreado=False; self.numJug=0     # jueCreado=creacion del juego; numJug=Numero de juadores entrantes
        self.timeIni=0; self.timeFin=0; self.hayGanador=False   # Tiempo de inicio y fin;y si hay ganador
        self.marcas=list(); self.numPlay=0  # marcas=Marca de los jugadores; numPlay=numero de jugadores 
        self.pool=ActivePool(); self.ganador="" # pool=objeto de los candados
        self.sema=threading.Semaphore(1)    # creacion del semaforo

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
                    productor.start()   # Hilo para crear juego
                
                if self.numJug>0 and client_addr!=self.jugA[0]:
                    self.jugA.append(client_addr)
                    self.numJug+=1; i+=1
                    resto=threading.Thread(target=self.resto,
                                                args=[client_conn,client_addr,self.numJug],
                                                name='Resto-'+str(i))
                    resto.start()   # Hilo de espera del juego

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
        for i in range(self.numPlay):   # Creacion de las marcas
            self.marcas.append("-")
        m=str(conn.recv(1024).decode()) # Marca del jugador
        self.marcas[0]=m
        logging.debug("Jugadores: "+str(self.numPlay))
        response=bytes("Bienvenido al juego de gato\n"+
                        "Elige la dificultad del juego\n"+
                        "1. Principiante\n2. Avanzado", 'ascii')
        conn.sendall(response)
        tam=conn.recv(1024)
        # Creacion del juego
        if int(tam.decode())==1:
            self.k=3; self.juego=Gato(self.k,self.numPlay)
            self.jueCreado=True
        elif int(tam.decode())==2:
            self.k=5; self.juego=Gato(self.k*2,self.numPlay)
            self.jueCreado=True
        logging.debug("Juego creado: "+str(self.jueCreado))
        logging.debug("Tamanio: "+str(len(self.hilos))+" Juego: "+str(self.jueCreado))
        while True:
            if len(self.hilos)==self.numPlay and self.jueCreado:
                logging.debug("Hecho, creando jugadores.")
                self.timeIni=time.time()    # Inicio del juego
                self.juego.marcas=self.marcas
                # Inicio de los jugadores y partida
                for t in self.hilos:
                    self.juego.marcas.append("-")
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
        dato=conn.recv(1024)
        m=str(dato.decode())
        logging.debug("Podemos continuar")
        while True: 
            if len(self.hilos)==self.numPlay: #and self.jueCreado:
                self.marcas[num-1]=m
                conn.sendall(str.encode("gogo"))
                break
            time.sleep(1)

    def mandarTablero(self,conn):   # Mandar tablero del juego
        tablero=self.juego.verGato()
        response=str.encode(str(tablero))
        conn.sendall(response)

    def recibir_datos(self,fi,conn,addr,pool,s):
        logging.debug('Creado')
        try:
            time.sleep(1)
            self.mandarTablero(conn)    # Mandar tablero
            time.sleep(1.5)
            conn.sendall(str.encode("wt"))  # Espera de turno
            while not self.hayGanador:
                logging.debug("Espero turno")
                time.sleep(1)
                with s:
                    if not self.hayGanador:
                        self.mandarTablero(conn)    # Mandar tablero
                        name=threading.currentThread().getName()
                        time.sleep(1)
                        pool.makeActive(name,conn,fi,self.juego)    # Espera de tiro
                        time.sleep(1)
                        self.hayGanador,self.ganador=pool.makeInactive(name,fi,self.juego,self.k)   # Verificacion del juego
                        for i in self.listaConexiones:  # Manda actualizacion del tiro
                            self.mandarTablero(i)
                            time.sleep(1)
                            i.sendall(str.encode("wt"))
                    elif self.hayGanador and not self.fin:  # Mandar ultimos mensajes
                        time.sleep(1)
                        i.sendall(str.encode("exit"))
                        time.sleep(1)
                        i.sendall(str.encode("\n\tEl ganador es el {}\n\t\t¡¡Felicidades!!").format(self.ganador))  # Manda ganador
                        self.fin=True; pool.libera()
                    time.sleep(1)
            self.timeFin=time.time()
            lastMsg=self.juego.tiempoPartida(self.timeFin-self.timeIni)
            conn.sendall(str.encode(lastMasg))  # Manda tiempo del juego
        except Exception as e:
            print(e)
        finally:
            self.numJug-=1;
            print("Conexion cerrada por {}".format(addr))
            conn.close()    # Cierra conexion

s=Servidor()