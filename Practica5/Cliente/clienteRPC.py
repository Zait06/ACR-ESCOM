import sys
import getpass
import datetime
import xmlrpc.client

HOST=sys.argv[1]; PORT=sys.argv[2]
addr=HOST+':'+PORT
s = xmlrpc.client.ServerProxy('http://'+addr)  # Quien atiende las solicitudes
orden=""; instruc=list()

print("\tSERVICIO RPC")
nueva=input('Presione [M] si es que cuenta con un perfil, sino,\npresione [N] para crear una nueva cuenta: ')
user=input("Usuario: ")
pasw=getpass.getpass("Contraseña: ")

if nueva.upper()=='M':
    ing=s.signIn(user,pasw)
else:
    ing=s.logIn(user,pasw)

if ing:
    print('\tSesión iniciada\n')
    while True:
        orden=input("user@"+user+">> ")
        instruc=orden.lower().split()
        try:
            if instruc[0]=='null':                                  # Hace un ping con el servidor
                print(s.hacerPing())
            elif instruc[0]=='create':                              # Crear un archivo
                print(s.crearArchivo(instruc[1],user))
            elif instruc[0]=='read':                                # Lee un archivo
                print(s.leerArchivo(user,instruc[1]))
            elif instruc[0]=='write':                               # Edita un archivo
                dato=input('Ingrese un texto:\n->')
                print(s.editarArchivo(user,instruc[1],dato))
            elif instruc[0]=='rename':                              # Cambia nombre al archivo
                print(s.renombrar(instruc[1],instruc[2],user))
            elif instruc[0]=='remove':                              # Elimina un archivo
                print(s.borrarArchivo(instruc[1],user))
            elif instruc[0]=='mkdir':                               # Crea una carpeta
                print(s.crearCarpeta(instruc[1],user))
            elif instruc[0]=='rmdir':                               # Elimina una carpeta
                print(s.borrarCarpeta(instruc[1],user))
            elif instruc[0]=='readdir':                             # Vista de todos los archivos
                print(s.verContenido(user))
            elif instruc[0]=='getattr':                             # Informacion del archivo
                print(s.infoArchivo(instruc[1],user))
            elif instruc[0]=='pwd':                                 # Direccion del usuario
                print(s.verDireccion(user))
            elif instruc[0]=='exit':                                # Salir de todo
                print("\n\t\tHASTA PRONTO "+user+"\n")
                break
            else:
                print("Instruccion incorrecta, intente de nuevo\n")
        except Exception as e:
            print(e)
else:
    print("Usuario o contraseña incorrectas")