from instrucciones import *
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):   # Escucha a todos los solicitantes http
    rpc_paths = ('/RPC2',)  # Ruta principal

# Crea el servidor RPC
with SimpleXMLRPCServer(('localhost', 8080),requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    server.register_instance(Instrucciones()) # La clase se registra con todos sus metodos de forma xml

    server.serve_forever()