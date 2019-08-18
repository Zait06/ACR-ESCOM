"""
    Hernández López Ángel Zait
    Juego de gato
"""

import numpy as np
import random as rand
import os

class Gato:
    def __init__(self):
        self.t=np.zeros((3,3),dtype=np.int)     # Matriz inicial de ceros
        self.p=""                               # Coordenadas a guardar
        self.xy=[]                              # Coordenadas a guardar en enteros

    def bienvenida(self):   # Mensaje de bienvenida
        print("Bienvenido al juego de gato\n")

    def verGato(self):  # Muestra del tablero
        return str(self.t)
    
    def jugadaP1(self): # Jugada del jugador 1
        self.p=input("\nIngrese las coordenadas donde desea tirar: ")
        return self.p
        
    def jugadaP2(self): # Jugada del jugador 2 (maquina)
        a=rand.randint(0,2) # Numeros al azar donde poner el número
        b=rand.randint(0,2)
        if self.t[a][b]==0: # Si está vacío, ingrese el número
            self.t[a][b]=(-1)
        else:   # Si no, busque otras coordenadas
            self.jugadaP2()
        
    def verifica(self,tipo):    # Verifica si hay un ganador
        ganador=False
        gan=np.array([tipo,tipo,tipo])  # Hace una copia del vector ganador
        for i in range(3):  # Pasa por toda la matriz
            if (self.t[i,:]==gan).all():    # Verifica filas completas
                ganador=True
            elif (self.t[:,i]==gan).all():  # Verifica columnas completas
                ganador=True
        if (np.diag(self.t)==gan).all():    # Diagonal de la matriz
            ganador=True
        elif (np.diag(np.fliplr(self.t))==gan).all():   # Diagonal inversa
            ganador=True
        return ganador  # Devuelve verdadero si es que alguien ganó