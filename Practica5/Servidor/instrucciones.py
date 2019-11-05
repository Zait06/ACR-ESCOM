import os
import sys

# http://archive.download.redhat.com/pub/redhat/linux/7.1/es/doc/RH-DOCS/es/rhl-gsg-es-7.1/ch-doslinux.html

os.chdir('user')

class Instrucciones:
    def signIn(self,usua,pasw):
        perfil=list(); simon=False
        f=open("../perfiles.txt","r")
        for linea in f.readlines():
            perfil=str(linea).split(':')
            if perfil[0]==usua and perfil[1]==(str(pasw)+"\n"):
                simon=True
                break
        f.close()
        return simon

    def eleccion(self, inst):
        self.ins=inst.split()

    def verDireccion(self):
        return str(os.getcwd())
    
    def verContenido(self):
        return str(os.listdir())
    
    def crearArchivo(self,arch):
        f=open(arch,"w")
        f.close()
        return self.verContenido()

    def crearCarpeta(self,nombre):
        os.mkdir(str(nombre))
        return self.verContenido()

    def copiarArch(self):
        return 'copiado'