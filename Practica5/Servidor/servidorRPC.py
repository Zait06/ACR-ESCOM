from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):   # Escucha a todos los solicitantes http
    rpc_paths = ('/RPC2',)  # Ruta principal

# Crea el servidor RPC
with SimpleXMLRPCServer(('localhost', 8000),requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    class MyFuncs:
        def mul(self, x, y):
            return x * y

        def show_type(self, arg):
            return (str(arg), str(type(arg)), arg)

    server.register_instance(MyFuncs()) # La clase se registra con todos sus metodos de forma xml

    server.serve_forever()