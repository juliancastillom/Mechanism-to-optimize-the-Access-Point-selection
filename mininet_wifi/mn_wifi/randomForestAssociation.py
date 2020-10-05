#!/usr/bin/env python
# coding: utf-8
import pickle
import time

print("Loading - Random Forest Model")
filename = '/home/mininet/mininet-wifi/mn_wifi/models_ml/random_forest_model_V2.sav'
# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
print("Loaded - Random Forest Model")

def pred(info):
	tiempo_inicial = time.time() 
	sol = loaded_model.predict(info)
	tiempo_final = time.time()
	time_selec = tiempo_final - tiempo_inicial
	print("time: " + str(time_selec*1000))
	print ("solution: " + str(sol))
	return(sol)
