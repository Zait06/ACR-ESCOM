import tftpy
# se crea la instancia del servidor tftp
# el unico parametro es la ruta donde estara la carpeta o directorio donde se almacenaran nuestros archivos
server = tftpy.TftpServer('./recursosTFTP')
print('Servidor iniciado')
server.listen('127.0.0.1', 6969)