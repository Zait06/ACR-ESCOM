import xmlrpc.client
import datetime
import getpass

s = xmlrpc.client.ServerProxy('http://127.0.0.1:8080')  # Quien atiende las solicitudes
orden=""; instruc=list()

user=input("Usuario: ")
pasw=getpass.getpass("Contraseña: ")
ing=s.signIn(user,pasw)

while ing:
    orden=input("user@"+user+">>")
    instruc=orden.lower().split()
    
    try:
        if instruc[0]=='null':
            print(s.hacerPing())
        elif instruc[0]=='create':
            print(s.crearArchivo(instruc[1]))
        elif instruc[0]=='mkdir':
            print(s.crearCarpeta(instruc[1]))
        elif instruc[0]=='rmdir':
            print(s.borrarCarpeta(instruc[1]))
        elif instruc[0]=='readdir':
            print(s.verContenido())
        elif instruc[0]=='pwd':
            print(s.verDireccion())
        elif instruc[0]=='exit':
            break
        else:
            print("Instruccion incorrecta, intente de nuevo\n")
    except Exception as e:
        print(e)
else:
    print("Usuario o contraseña incorrectas")