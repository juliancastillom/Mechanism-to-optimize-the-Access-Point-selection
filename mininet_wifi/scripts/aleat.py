#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  aleat.py
from random import randint
import time
import math

#movimiento aleatorio
def generate():
	x = 0
	y = 0
	z = 0
	for i in xrange(250):
		x += randint(0,2)*(1)**randint(0, 1)
		y += randint(0,4)*(1)**randint(0, 1)
		print("{} {},{},{}".format(i, x, y, z))

	"""u1_start = '10.0,150.0,0'
	u1_stop = '160.0,170.0,0'
	
	u2_start = '25.0,70.0,0'
	u2_stop = '90.0,150.0,0'
	"""
	
#movimiento lineal
def generateU1():
	x_ini = 32.0
	y_ini = 112.0
	z_ini = 0.0
	x_fin = 140.0
	y_fin = 166.0
	z_fin = 0.0
	x = x_ini
	y = y_ini
	z = z_ini
	num_pasos = 60
	f= open("u5_mov.txt","w+")
	for i in xrange(num_pasos):
		x = x + (x_fin-x_ini)/num_pasos
		y = y + (y_fin-y_ini)/num_pasos
		print("{} {},{},{}".format(i, x, y, z))
		f.write("{} {},{},{} \n".format(i, x, y, z))
	f.close()


def generateU2():
	x_ini = 25.0
	y_ini = 70.0
	z_ini = 0.0
	x_fin = 90.0
	y_fin = 150.0
	z_fin = 0.0
	x = x_ini
	y = y_ini
	z = z_ini
	num_pasos = 250
	
	for i in xrange(num_pasos):
		x = x + (x_fin-x_ini)/num_pasos
		y = y + (y_fin-y_ini)/num_pasos
		print("{} {},{},{}".format(i, x, y, z))

#movimiento circular
def generateCircle():
	x_ini = 60.1
	y_ini = 150.0
	z_ini = 0.0
	x_fin = 60.1
	y_fin = 150.0
	z_fin = 0.0
	r = 30
	pi = math.pi
	rad = 2*pi*r
	x = x_ini
	y = y_ini
	z = z_ini
	num_pasos = int(rad)
	
	alfa = 90
	beta = 150
	
	grad_paso = 360.0/float(num_pasos)
	rad_paso = math.radians(grad_paso)
	
	x = r*math.cos(rad_paso)
	y = r*math.sin(rad_paso)
	
	print ("Perimetro: " + str(rad) + ("m"))
	print ("Numero pasos: " + str(num_pasos))
	print ("Grados por paso: " + str(grad_paso) + "ª")
	print ("Radianes por paso: " + str(rad_paso) + "rad")
	print ("x: " + str(x) + "m")
	print ("y: " + str(y) + "m")
	print ("x-2: " + str(x + alfa) + "m")
	print ("y-2: " + str(y + beta) + "m")
	
	rad_paso2 = rad_paso
	f= open("archivo.txt","w+")
	for i in xrange(num_pasos):
		x = r*math.cos(rad_paso2) + alfa
		y = r*math.sin(rad_paso2) + beta
		print("{} {},{},{}".format(i, x, y, z))
		rad_paso2 = rad_paso2 + rad_paso
		f.write("{} {},{},{} \n".format(i, x, y, z))
	f.close()


def generateCircle2():
	x_ini = 60.1
	y_ini = 150.0
	z_ini = 0.0
	x_fin = 60.1
	y_fin = 150.0
	z_fin = 0.0
	r = 30
	pi = math.pi
	rad = 2*pi*r
	x = x_ini
	y = y_ini
	z = z_ini
	num_pasos = int(rad)
	
	alfa = 90
	beta = 150
	
	grad_paso = 360.0/float(num_pasos)
	rad_paso = math.radians(grad_paso)
	
	x = r*math.cos(rad_paso)
	y = r*math.sin(rad_paso)
	
	print ("Perimetro: " + str(rad) + ("m"))
	print ("Numero pasos: " + str(num_pasos))
	print ("Grados por paso: " + str(grad_paso) + "ª")
	print ("Radianes por paso: " + str(rad_paso) + "rad")
	print ("x: " + str(x) + "m")
	print ("y: " + str(y) + "m")
	print ("x-2: " + str(x + alfa) + "m")
	print ("y-2: " + str(y + beta) + "m")
	
	rad_paso2 = rad_paso
	f= open("sta_output/archivo.txt","w+")
	for i in xrange(num_pasos):
		x = r*math.cos(rad_paso2) + alfa
		y = r*math.sin(rad_paso2) + beta
		print("{} {},{},{}".format(i, x, y, z))
		rad_paso2 = rad_paso2 + rad_paso
		f.write("{} {},{},{} \n".format(i, x, y, z))
		time.sleep(0.2)
	f.close()

generateU1()
print("tiempo Final")
print(time.strftime("%H:%M:%S"))
