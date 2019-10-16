import os
import json
import argparse
import http.client
REMOTE_SERVER_HOST = '127.0.0.1:8080'
REMOTE_SERVER_PATH = '/'

conn = http.client.HTTPConnection(REMOTE_SERVER_HOST)
conn.request("GET", "/")

os.system("clear")

print("--- Metodo GET ---")
r1 = conn.getresponse()
print(r1.status, r1.reason)
data1 = r1.read()  # This will return entire content.
conn.request("GET", "/")
r1 = conn.getresponse()
while True:
     chunk = r1.read()
     if not chunk:
          break
     print(chunk.decode())

print("\n\n--- Metodo HEAD ---")
conn.request("HEAD","/")
r2=conn.getresponse()
print(r2.status, r2.reason)
print(r2.read().decode()=='')

print("\n\n--- Metodo POST ---")
nombre=input("Ingrese un nombre: ")
headers = {'Content-type': 'application/json'}
foo = {'text': 'Hola '+nombre}
json_data = json.dumps(foo)
conn.request('POST', '/', json_data, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
print(r1.read().decode())

conn.close()