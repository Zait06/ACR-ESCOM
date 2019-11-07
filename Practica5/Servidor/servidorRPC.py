import sys
from instrucciones import *
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

HOST=sys.argv[1]; PORT=int(sys.argv[2])

class RequestHandler(SimpleXMLRPCRequestHandler):   # Escucha a todos los solicitantes http
    rpc_paths = ('/RPC2',)  # Ruta principal

# Crea el servidor RPC
with SimpleXMLRPCServer((HOST,PORT),requestHandler=RequestHandler) as server:
    print("Servidor a la escucha")
    server.register_introspection_functions()

    server.register_instance(Instrucciones()) # La clase se registra con todos sus metodos de forma xml

    server.serve_forever()