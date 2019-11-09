import os
import time

os.chdir('user')

class Instrucciones:
    def signIn(self,usua,pasw):                     # Ingresar con un usuario
        perfil=list(); simon=False
        f=open("../perfiles.txt","r")               # Abrir archivo de perfiles
        for linea in f.readlines():
            perfil=str(linea).split(':')
            if perfil[0]==usua and perfil[1]==(str(pasw)+"\n"): # Verificación de su existencia
                simon=True
                break
        f.close()                                   # Cierre el archivo
        return simon

    def logIn(self,usua,pasw):                      # Registrar nuevo usuario
        simon=False
        try:
            with open("../perfiles.txt","a") as f:  # Abrir archivo para agregar un nuevo miembro
                f.write(usua+':'+pasw+'\n')
            os.mkdir(usua)                          # Se crea una carpeta para el nuevo miembro
            with open("./"+usua+"/inicio.txt",'w') as f:    # Da archivo de bienvenida
                f.write("Bienvenid@ "+usua+" al servicio RPC")
            simon=True
        except Exception as e:
            print(e)
            simon=False
        return simon

    def hacerPing(self):                            # null - ping
        return 'Conectado al servidor'

    def crearArchivo(self,arch,usua):               # create
        f=open("./"+usua+"/"+arch,"w")              # Abre y cierra un archivo
        f.close()
        return self.verContenido(usua)
    
    def ordenLookUp(self,usua,ficha):               # lookup
        encon="Elemento inexistente"
        conten=os.listdir(usua)
        for dd in conten:
            if dd==ficha:
                encon="Elemento encontrado"
                break
        return encon

    def leerArchivo(self,usua,arch):                # read
        envio=str.encode('')
        with open("./"+usua+"/"+arch,"rb") as f:
            for linea in f.readlines():
                envio=envio+linea
        return envio

    def editarArchivo(self,usua,arch,texto):        # write
        with open("./"+usua+"/"+arch,"a") as f:
            f.write(texto+'\n')
        return self.leerArchivo(usua,arch)

    def renombrar(self,nom1,nom2,usua):             # rename
        os.rename("./"+usua+"/"+nom1,"./"+usua+"/"+nom2)
        return self.verContenido(usua)

    def borrarArchivo(self,nom,usua):               # remove
        os.remove("./"+usua+"/"+nom)
        return self.verContenido(usua)

    def crearCarpeta(self,nombre,usua):             # mkdir
        os.mkdir("./"+usua+"/"+nombre)
        return self.verContenido(usua)

    def borrarCarpeta(self,nombre,usua):            # rmdir
        os.rmdir("./"+usua+"/"+nombre)
        return self.verContenido(usua)

    def verContenido(self,usua):                    # readdir
        return str(os.listdir(usua))

    def infoArchivo(self,nombre,usua):              # getattr
        mensaje="\t"+nombre
        tama=os.path.getsize("./"+usua+"/"+nombre)
        hora=os.path.getmtime("./"+usua+"/"+nombre)
        mensaje=mensaje+'\n\tFecha de modificado: '+str(time.ctime(hora))
        mensaje=mensaje+'\n\tTamaño: '+str(tama)+' bytes'
        mensaje=mensaje+'\n\t'+os.getcwd()+"/"+usua
        return mensaje

    def accesoPath(self,usua):                      # access
        req="Acceso para el usuario "+usua
        return req

    def verDireccion(self,usua):                    # pwd
        return os.getcwd()+"/"+usua