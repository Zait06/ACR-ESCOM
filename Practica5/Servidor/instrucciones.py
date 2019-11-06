import os
import sys

# http://archive.download.redhat.com/pub/redhat/linux/7.1/es/doc/RH-DOCS/es/rhl-gsg-es-7.1/ch-doslinux.html

os.chdir('user')

class Instrucciones:
    def __init__(self):
        self.direc=''

    def signIn(self,usua,pasw):
        perfil=list(); simon=False
        f=open("../perfiles.txt","r")
        for linea in f.readlines():
            perfil=str(linea).split(':')
            if perfil[0]==usua and perfil[1]==(str(pasw)+"\n"):
                simon=True
                break
        f.close()
        self.direc=usua
        return simon

    def hacerPing(self):
        return 'Conectado'

    def verDireccion(self):
        return str(os.getcwd())
    
    def verContenido(self):
        return str(os.listdir())
    
    def crearArchivo(self,arch):
        f=open(arch,"w")
        f.close()
        return self.verContenido()

    def renomCarpeta(self,nom1,nom2):
        os.rename(nom1,nom2)
        return self.verContenido()

    def crearCarpeta(self,nombre):
        os.mkdir(str(nombre))
        return self.verContenido()

    def borrarCarpeta(self,nombre):
        os.rmdir(nombre)
        return self.verContenido()