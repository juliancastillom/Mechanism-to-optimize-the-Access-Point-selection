#!/usr/bin/python
#Leer archivo y contar el numero de efetos ping-pong

import json
#archivo = open("/home/mininet/Escritorio/scripts/output/ssf.txt")
#archivo = open("/home/mininet/Escritorio/scripts/output/llf.txt")
#archivo = open("/home/mininet/Escritorio/scripts/output/slf.txt")
archivo = open("/home/mininet/Escritorio/scripts/output/topsis.txt")
#archivo = open("/home/mininet/Escritorio/scripts/output/saw.txt")
a = 0
suma = 0.

old1 = ""
new1 = ""
sta1 = ""

old2 = ""
new2 = ""
sta2 = ""

pp = 0
npp = 0

for linea in archivo.readlines():
	#d= linea
	"""print(type(d))
	print (d)
	"""
	print("---")
	#print ("1 - " + oldnew)
	print "old1 = " + old1
	print "new1 = " + new1
	print "sta1 = " + sta1
	d = json.loads(linea)
	old2 = str(d.get('oldAp'))
	new2 = str(d.get('newAp'))
	sta2 = str(d.get('sta'))
	#print ("2 - " + oldnew)
	print "old2 = " + old2
	print "new2 = " + new2
	print "sta2 = " + sta2
	
	if (old1 == new2 and new1 == old2 and sta1 == sta2):
		pp = pp +1
		print("ping pong")
	else:
		npp = npp +1
		print("NO NO NO NO NO NO NO NO ping pong")
	
	old1 = str(old2)
	new1 = str(new2)
	sta1 = str(sta2)
	
	#print (d)
	#print(type(d))
	#print (a)
	#print( float(d.get('time')) )
	suma = suma + float(d.get('time'))
	a = a+1
	print a
	print( float(d.get('time')) )
	print suma
	prom = suma/a
	print(prom)
	print
	#print(d.keys())
print "suma total tiempo = " + str(suma)
print "num handover = " + str(a)
print "promedio tiempo = " + str(prom)
print "num efectos ping pong = " + str(pp)
print "num NO efectos ping pong = " + str(npp)
archivo.close()
