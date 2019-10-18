import tftpy
# se crea la instancia del cliente tftp
# el primer parametro es la ip o el dominio del servidor
# el segundo parametro es el puerto por el cual escucha nuestro servidor
client = tftpy.TftpClient('127.0.0.1', 6969)
# se inicia un ciclo while infinito
while (True):
	# por consola se pide que el usuario ingrese el comando put/get y el nombre de los archivos
	# ejemplo : get algo1.txt algo2.txt 
	inputString = raw_input("tftp> ")
	# de la cadena de entrada del paso anterior se sub-divide para obtener el nombre del archivo 1 y archivo 2   
	file1 = inputString[4: (inputString[4:].find(" ") + 4) ]
	file2 = inputString[ (inputString[4:].find(" ") + 1 + 4) : ]
	# si el usuario inicia su cadena con "put" esto quiere decir que subira un archivo al servidor
	if inputString[:3] == 'put':
		# funcion la cual cargara un archivo al servidor
		# el primer parametro es el nombre del archivo tal como se encuentra en nuestro lado del cliente
		# el segundo parametro es como renombraremos al archivo del lado del servidor
		client.upload(file1, file2)
	# si el usuario inicia su cadena con "get" esto quiere decir que bajara un archivo del servidor
	elif inputString[:3] == 'get':
		# funcion la cual descarga el archivo desde el servidor
		# el primer parametro es el nombre del archivo tal como se encuentra en el servidor
		# el segundo parametro es como renombraremos al archivo de nuestro lado del cliente
		client.download(file1, file2)
	else:
		# si la cadena no tiene el formato deseado se imprimira esta pantalla y se continuara en el ciclo
		print("Formato desconocido")

	 