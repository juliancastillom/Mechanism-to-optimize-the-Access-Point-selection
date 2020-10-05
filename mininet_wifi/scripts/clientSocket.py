#!/usr/bin/env python

#Variables
host = '10.0.0.6'
port = 8050
#Se importa el modulo
import socket
import time
 
#Creacion de un objeto socket (lado cliente)
obj = socket.socket()
 
#Conexion con el servidor. Parametros: IP (puede ser del tipo 192.168.1.1 o localhost), Puerto
obj.connect((host, port))
print("Conectado al servidor")
 
#Creamos un bucle para retener la conexion
while True:
	#Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
	#mens = raw_input("Mensaje desde Cliente a Servidor >> ")
	#obj.send(mens)
	i = 0
	while i < 10:
		mens = "Mensaje desde Cliente a Servidor >> %s" % i
		print(str(mens))
		i = i + 1
		obj.send(mens)
		time.sleep(0.5)
	else:
		obj.close()
		print('socket cliente cerrado')
	"""
	if str(mens) == "close()":
		obj.close()
		print('socket cliente cerrado')
	#Con el metodo send, enviamos el mensaje
	"""

#Cerramos la instancia del objeto servidor
obj.close()

#Imprimimos la palabra Adios para cuando se cierre la conexion
print("Conexion cerrada")
