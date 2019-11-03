import os
import sys

class Instrucciones:
    def __init__(self):
        self.mensaje=list()
        self.orden=['crear','mover','copiar']
        self.winOrd=['mkdir','put']

    def eleccion(self, inst):
        self.ins=inst.split()

    def show_type(self, arg):
        return (str(arg), str(type(arg)), arg)