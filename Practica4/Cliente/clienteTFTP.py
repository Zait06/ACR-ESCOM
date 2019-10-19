import tftpy
# se crea la instancia del cliente tftp
# el primer parametro es la ip o el dominio del servidor
# el segundo parametro es el puerto por el cual escucha nuestro servidor
client=tftpy.TftpClient('127.0.0.1', 6969)
# se inicia un ciclo while infinito
while (True):
	# ejemplo : get algo1.txt algo2.txt
	# el primer parametro es como renombraremos al archivo del lado del servidor
	# el segundo parametro es el nombre del archivo tal como se encuentra en nuestro lado del cliente
	inputString=raw_input("tftp> ")
	splitString=inputString.split() # print(splitString)
	try:
		if splitString[0].lower()=='put':
			# funcion la cual cargara un archivo al servidor
			client.upload(splitString[1],splitString[2])
		elif splitString[0].lower()=='get':
			# funcion la cual descarga el archivo desde el servidor
			client.download(splitString[1],splitString[2])
		elif splitString[0].lower()=="exit":
			print("Desconectado")
			break
		else:
			print("Formato desconocido")
	except Exception as e:
		print(e)
		infoERR=tftpy.TftpPacketTypes.TftpPacketERR()
		print(infoERR)

	 