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
        self.tt=["-"]*4

    def bienvenida(self):   # Mensaje de bienvenida
        print("Bienvenido al juego de gato\n")

    def verGato(self):  # Muestra del tablero
        for i in range(4):
            tabla=""
            for j in range(4):
                tabla=tabla+str(self.tt[i][j])+" "
            print(tabla)

    
    def jugadaP1(self): # Jugada del jugador 1
        self.p=input("\nIngrese las coordenadas donde desea tirar: ")
        self.xy=self.p.split(",")   # Separación del string recibido
        if self.t[int(self.xy[0])][int(self.xy[1])]==0: # Si es que la casilla está vacía, ingrese el numero
            self.t[int(self.xy[0])][int(self.xy[1])]=1
            self.tt[int(self.xy[0])+1][int(self.xy[1])+1]="X"
        else:   # Si no es así, ingrese de nuevo otras coordenas
            os.system ("clear")
            print("Lugar ocupado\n")
            self.verGato()
            self.jugadaP1()

    def jugadaP2(self): # Jugada del jugador 2 (maquina)
        a=rand.randint(0,2) # Numeros al azar donde poner el número
        b=rand.randint(0,2)
        if self.t[a][b]==0: # Si está vacío, ingrese el número
            self.t[a][b]=(-1)
            self.tt[a+1][b+1]="O"
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

    def llenoTT(self):
        for i in range(4):
            self.tt[i]=["-"]*4
        self.tt[1][0]=0
        for i in range(3):
            for j in range(3):
                if i==0:
                    self.tt[i][j+1]=j
                elif j==0:
                    self.tt[i+1][j]=i


sig1=False; sig2=False  # Variables para seguir o no jugando y verificar al ganador
tirosP1=0; tirosP2=0    # Numero de tiros que lleva cada jugador
cat=Gato()              # Se crea el objeto Gato llamado cat
cat.llenoTT()
cat.bienvenida()        
while(True):
    cat.verGato()

    cat.jugadaP1()
    tirosP1+=1          # Realizada la jugada, se suma un turno
    if tirosP1>=2:      # Si el turno supera los 2, se verifica si es candidato a ganar
        sig1=cat.verifica(1)
    if sig1:            # Si es verdadero, acaba el juego y el ganador es el jugador 1
        cat.verGato()
        print("\n\tEl ganador es el jugador 1!!!\n")
        break
    elif tirosP1>=4 and tirosP2>=4: # si los tiros sobrepasan los 4 turnos, o bien, se llena la matriz, acaba la partida
        cat.verGato()
        print("\n\tGato!!!\n")
        break

    cat.jugadaP2()
    tirosP2+=1          # Realizada la jugada, se suma un turno
    if tirosP2>=2:      # Si el turno supera los 2, se verifica si es candidato a ganar
        sig2=cat.verifica(-1)
    if sig2:            # Si es verdadero, acaba el juego y el ganador es el jugador 2
        cat.verGato()
        print("\n\tEl ganador es el jugador 2!!!\n")
        break
    else:               # Si nada de lo anterior se cumple, se sigue jugando hasta que haya un ganador
        os.system ("clear")

print("\t\tFin del juego Dx\n")

