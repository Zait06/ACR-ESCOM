import os
import sys

# http://archive.download.redhat.com/pub/redhat/linux/7.1/es/doc/RH-DOCS/es/rhl-gsg-es-7.1/ch-doslinux.html

os.chdir('user')

class Instrucciones:
    def eleccion(self, inst):
        self.ins=inst.split()

    def verDireccion(self):
        return str(os.getcwd())
    
    def verContenido(self):
        return str(os.listdir())

    def crearCarpeta(self,nombre):
        os.mkdir(str(nombre))
        return self.verContenido()

    def copiarArch(self):
        return 'copiado'