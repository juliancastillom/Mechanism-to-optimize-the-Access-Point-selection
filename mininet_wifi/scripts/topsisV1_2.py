#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  topsisV1_2.py

import numpy as np
from time import time

a1 = np.array([5, 8, 4])
a2 = np.array([7, 6, 8])
a3 = np.array([8, 8, 6])
a4 = np.array([7, 4, 6])
p = np.array([0.3, 0.4, 0.3])
n = 4


a1 = np.array([5, 8, 4, 5, 8, 4, 5, 8, 4, 5, 8, 4])
a2 = np.array([19, 19, 18, 17, 19, 18, 19, 19, 18, 17, 19, 18])
a3 = np.array([8, 8, 6, 8, 8, 6, 8, 8, 6, 8, 8, 6])
a4 = np.array([17, 14, 16, 17, 14, 16, 17, 14, 16, 17, 14, 16])
p = np.array([0.3, 0.4, 0.3, 0.3, 0.4, 0.3, 0.3, 0.4, 0.3, 0.3, 0.4, 0.3])
n = 4


tiempo_inicial = time() 
#crear matriz de decision
m1 = np.array([a1, a2, a3, a4])
#a2D = np.array([[1,2,3],[1,2,3]])

#print(m1[2,0]**2)


#n = m1[0,0]/( ( (m1[0,0]**2) + (m1[1,0]**2) + (m1[2,0]**2))**(0.5) )
#n = ( ( (m[0,0]**2) + (m[1,0]**2) + (m[2,0]**2))**(1/2) )
#n = (m[0,0]**2) + (m[1,0]**2) + (m[2,0]**2)
#n = n**(0.5)

#m2 = m1
m12 = m1**2

#print(m1[0:,0])

#divisor de cada columna
m13 = m12.sum(axis=0)**(0.5) 

#matriz normalizada de decision
m2 = m1/m13

#matriz normalizada de pesos
m3 = m2 * p

#maximos y minimos de casa columna
m31 = m3.max(axis=0)
m32 = m3.min(axis=0)


#Calcular la separacion de la SOLUCION IDEAL POSITIVA Y NEGATIVA (PIS)(NIS) 

#PIS
m411 = m3 - m31

m421 = m411**2


m431 = m421.sum(axis=1)**(0.5) 

#NIS

m412 = m3 - m32

m422 = m412**2


m432 = m422.sum(axis=1)**(0.5) 


m45 = np.array([m431,m432])

#m4 = m45.transpose()
m4 = m45

# cercania relativa a la solucion ideal
#m51 = m4.sum(axis=1)
m51 = m4.sum(axis=0)


m5 = m4[1,0:]/m51
# orden de redes de peor a mejor

#mejor red
print('\n---Valor mejor red')
print(m5.max())
#Posicion del argumento maximo
print('\n---posicion mejor red')
print(m5.argmax())

tiempo_final = time() 
 
tiempo_ejecucion = tiempo_final - tiempo_inicial
 
print 'El tiempo de ejecucion fue: %s ms' %(tiempo_ejecucion*1000)
