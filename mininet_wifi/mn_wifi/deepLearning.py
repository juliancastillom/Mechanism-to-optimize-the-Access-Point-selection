#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding: utf-8

from keras.models import Sequential, save_model, load_model
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.datasets import mnist
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import numpy as np

# Restore trained model
loaded_model = load_model('/home/mininet/mininet-wifi/mn_wifi/logs/model_deep')
loaded_model.load_weights('/home/mininet/mininet-wifi/mn_wifi/logs/weights.epoch.50-val_loss.0.15.hdf5')
print(loaded_model.summary())

def pred_dl(info):
	#tiempo_inicial = time.time() 
	sol = loaded_model.predict(info)
	sol = np.around(sol)
	sol = sol.astype(int)
	#tiempo_final = time.time()
	#time_selec = tiempo_final - tiempo_inicial
	#print(str(time_selec*1000))
	print (sol)
	return(sol)
