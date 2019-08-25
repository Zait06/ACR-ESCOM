"""
    Hernández López Ángel Zait
    Juego de gato
"""

import numpy as np
import random as rand
import os

class Gato:
    def __init__(self,tam):
        self.t=np.zeros((tam,tam),dtype=np.int)     # Matriz inicial de ceros
        self.xy=[]                              # Coordenadas a guardar en enteros

    def bienvenida(self):   # Mensaje de bienvenida
        print("Bienvenido al juego de gato\n")

    def verGato(self):  # Muestra del tablero
        return str(self.t)
    
    def jugadaP1(self): # Jugada del jugador 1
        p=input("\nIngrese las coordenadas donde desea tirar: ")
        return p
        
    def jugadaP2(self,tam): # Jugada del jugador 2 (maquina)
        if tam==5:
            tam=tam*2
        a=rand.randint(0,tam-1) # Numeros al azar donde poner el número
        b=rand.randint(0,tam-1)
        if self.t[a][b]==0: # Si está vacío, ingrese el número
            self.t[a][b]=(-1)
        else:   # Si no, busque otras coordenadas
            self.jugadaP2(tam)
        
    def verifica(self,tipo,tam):    # Verifica si hay un ganador
        ganador=False; rango=0
        gan=np.ones((tam),dtype=np.int)  # Hace una copia del vector ganador
        
        if tipo==(-1):                # Si es el jugador 2, lo verifica con -1
            gan=gan*-1
        
        if tam==3:
            ganador=self.veoCon3(gan)
        else:
            ganador=self.veoCon5(gan)

        return ganador

    def ocupado(self,coor,tipo):
        sip=False
        self.xy=coor.split(",")   # Separación del string recibido
        if self.t[int(self.xy[0])][int(self.xy[1])]==0: # Si es que la casilla está vacía, ingrese el numero
            self.t[int(self.xy[0])][int(self.xy[1])]=tipo
            sip=True
        else:
            sip=False
        return sip

    def veoCon3(self,gan):
        final=False
        for i in range(3):  # Pasa por toda la matriz
            if (self.t[i,:]==gan).all():    # Verifica filas completas
                final=True; break
            elif (self.t[:,i]==gan).all():  # Verifica columnas completas
                final=True; break
        if (np.diag(self.t)==gan).all():    # Diagonal de la matriz
            final=True
        elif (np.diag(np.fliplr(self.t))==gan).all():   # Diagonal inversa
            final=True
        return final  # Devuelve verdadero si es que alguien ganó
    
    def veoCon5(self,gan):
        final=False
        aux=np.zeros((5,5),dtype=np.int)    # Matriz auxiliar para verificar la diagonal de 5
        for i in range(10):  # Pasa por toda la matriz
            for j in range(5):
                if (self.t[i,j:j+5]==gan).all():    # Verifica filas completas
                    final=True; break
                elif (self.t[j:j+5,i]==gan).all():  # Verifica columnas completas
                    final=True; break
                if i<=5:
                    aux=self.t[i:i+5,j:j+5]
                    if (np.diag(aux)==gan).all():
                        final=True
                    elif (np.diag(np.fliplr(aux))==gan).all():
                        final=True
        return final  # Devuelve verdadero si es que alguien ganó

    def empate(self):
        if (self.t!=0).all():
            return True
        else:
            return False

    def tiempoPartida(self,tiempo): # Mensaje de tiemop
        mensaje="" 
        if tiempo<60:   # Si el tiempo es menor a los 60 seg. envia el mensaje
            mensaje="\tTiempo de juego: {0:.2f} seg.".format(float(tiempo))
        else:
            mensaje="\tTiempo de juego: {} min. ".format(int(tiempo/60))
            mensaje=mensaje+"{} seg.".format(int(tiempo%60))
        return mensaje