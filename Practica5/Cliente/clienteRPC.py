import xmlrpc.client
import datetime

s = xmlrpc.client.ServerProxy('http://localhost:8000')  # Quien atiende las solicitudes
orden=""; instruc=list()

while True:
    orden=input("user>> ")
    instruc=orden.lower().split()

    if instruc[0]=='ls' or instruc[0]=='dir':
        print(s.verContenido())
    elif instruc[0]=='mkdir' or instruc[0]=='md':
        print(s.crearCarpeta(instruc[1]))
    elif instruc[0]=='pwd':
        print(s.verDireccion())
    elif instruc[0]=='exit':
        break

'''
data = [
    ('boolean', True),
    ('integer', 1),
    ('float', 2.5),
    ('string', 'some text'),
    ('datetime', datetime.datetime.now()),
    ('array', ['a', 'list']),
    ('array', ('a', 'tuple')),
    ('structure', {'a': 'dictionary'}),
]

for t, v in data:
    as_string, type_name, value = s.show_type(v)
    print('{:<12}: {}'.format(t, as_string))
    print('{:12}  {}'.format('', type_name))
    print('{:12}  {}'.format('', value))

# Print list of available methods
print(s.system.listMethods())
'''