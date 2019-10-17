import os
import json
import argparse
import http.client

def aplicarGET(conn):
     print("--- Metodo GET ---")
     conn.request("GET","/")
     r = conn.getresponse()
     print(r.status, r.reason)
     print(r.read().decode())

def aplicarHEAD(conn):
     print("\n\n--- Metodo HEAD ---")
     conn.request("HEAD","/")
     r=conn.getresponse()
     print(r.status, r.reason)
     print("HEAD hecho? R=",str(r.read().decode()==''))

def aplicarPOST(coon):
     print("\n\n--- Metodo POST ---")
     nombre=input("Ingrese un nombre: ")
     apelli=input("Ingrese su apellido: ")
     headers = {'Content-type': 'application/json'}
     foo = {'nombre':nombre,'apellido':apelli}
     json_data = json.dumps(foo)
     conn.request('POST', '/post', json_data, headers)
     r1 = conn.getresponse()
     print(r1.status, r1.reason)
     print(r1.read().decode())

os.system("clear")

REMOTE_SERVER_HOST=input("Ingrese la 'ip:puerto' del servidor: ")
REMOTE_SERVER_PATH='/'

conn = http.client.HTTPConnection(REMOTE_SERVER_HOST)

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
          elif metodo.upper()=='EXIT':
               break
     except Exception as e:
          print(e)
     finally:
          conn.close()