import os
import json
import argparse
import http.client

def aplicarGET(conn):
     print("\n\n--- Metodo GET ---")
     conn.request("GET","/")
     r = conn.getresponse()
     print(r.status, r.reason)
     print(r.read().decode())

def aplicarHEAD(conn):
     print("\n\n--- Metodo HEAD ---")
     conn.request("HEAD","/")
     r=conn.getresponse()
     print(r.status, r.reason)
     print("HEAD hecho? R =",str(r.read().decode()==''))

def aplicarPOST(conn):
     print("\n\n--- Metodo POST ---")
     nombre=input("Ingrese un nombre: ")
     apelli=input("Ingrese su apellido: ")
     headers = {'Content-Type':'text/html'}
     foo = {'nombre':nombre,'apellido':apelli}
     json_data = json.dumps(foo)
     conn.request('POST', '/', json_data, headers)
     r = conn.getresponse()
     print(r.status, r.reason)
     print(r.read().decode())

def aplicarPUT(conn):
     print("\n\n--- Metodo PUT ---")
     conn.request("PUT","/","Metodo PUT")
     r=conn.getresponse()
     print(r.status, r.reason)
     print(r.read().decode())

os.system("clear")

REMOTE_SERVER_HOST=input("Ingrese la 'ip:puerto' del servidor: ")
REMOTE_SERVER_PATH='/'

conn = http.client.HTTPConnection(REMOTE_SERVER_HOST)
os.system("clear")

if conn:
     while True:
          metodo=input("\nIngrese el metodo deseado: ")
          os.system("clear")
          try:
               if metodo.upper()=='GET':
                    aplicarGET(conn)
               elif metodo.upper()=='HEAD':
                    aplicarHEAD(conn)
               elif metodo.upper()=='POST':
                    aplicarPOST(conn)
               elif metodo.upper()=='PUT':
                    aplicarPUT(conn)
               elif metodo.upper()=='EXIT':
                    break
               else:
                    print("Instruccion no encontrada, por favor, intente de nuevo.")
          except Exception as e:
               print(e)
          finally:
               conn.close()