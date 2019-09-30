import threading
import time

libros=["../libros/Bibla.txt","../libros/hamlet.txt","../libros/MobyDick.txt"]
leer=list()

def leerLibro(libro):
    archivo = open(libros[libro], "r")
    for linea in archivo.readlines():
        print(libros[libro]+" - "+linea)
        #time.sleep(0.1)

print("Tamanio: "+str(len(libros)))
time.sleep(3)
try:
    for i in range(3):
        t=threading.Thread(target=leerLibro,args=(i,))#,daemon=True)
        leer.append(t)
        t.start()
        t.join()
except:
    pass

#print(leer)

#for t in leer:
#   t.join()