"""

    Mininet-WiFi: A simple networking testbed for Wireless OpenFlow/SDWN!

author: 
Ramon Fontes (ramonrf@dca.fee.unicamp.br)
Daniela Embus
Julian Castillo


"""

from mininet.log import debug
import time
import sys
import os
import numpy as np
from randomForestAssociation import pred
from scipy import stats
import group_mobility as gm
from mn_wifi.link import wirelessLink, Association


class associationControl(object):
	"Mechanisms that optimize the use of the APs"
	
	changeAP = False
	#mens = 'no'
	
	def __init__(self, sta, ap, wlan, ac, ap_wlan):
		#print("association..........:" + str(ac))
		if ac in dir(self):
			self.__getattribute__(ac)(sta=sta, ap=ap, wlan=wlan, ap_wlan=ap_wlan)

	def llf(self, sta, ap, wlan, ap_wlan):
		#llf: Least loaded first
		tiempo_inicial = time.time() 
		apref = sta.params['associatedTo'][wlan]
		if apref != '':
			ref_llf = len(apref.params['associatedStations'])
			if len(ap.params['associatedStations']) + 2 < ref_llf:
				tiempo_final = time.time()
				time_selec = tiempo_final - tiempo_inicial
				debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
				sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
				self.changeAP = True
				print("**************************method execution**************************")
				f= open("/home/mininet/Escritorio/scripts/output/llf.txt","a+")
				#f.write('{"time":"%s","sta":"%s","oldAp":"%s", "newAp":"%s", "apsInRange":"%s","battery":"%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(ap.name), str(sta.params['apsInRange']), str(sta.params['battery'])))
				f.write('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(ap.name), str(sta.params['apsInRange']), str(sta.params['battery']), str(sta.params['position'])))
				print('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(ap.name), str(sta.params['apsInRange']), str(sta.params['battery']), str(sta.params['position'])))
				f.close()
				sta.params['battery'] = sta.params['battery'] - 0.1
				#print("assoc_py node: %s - battery: %s" % (sta.name, str(sta.params['battery'])))
		else:
			self.changeAP = True
		return self.changeAP

	def llf2(self, sta, ap, wlan, ap_wlan):
		#llf: Least loaded first
		apref = sta.params['associatedTo'][wlan]
		if apref != '':
			ref_llf = len(apref.params['associatedStations'])
			print('----------------------------')
			print('len AP-REF %s' % str(ref_llf))
			print('len AP-N %s' % str(len(ap.params['associatedStations'])))
			print('len AP-N +2 %s' % str(len(ap.params['associatedStations']) + 2))
			print('len AP-N compar %s' % str(len(ap.params['associatedStations']) + 2 < ref_llf))
			if len(ap.params['associatedStations']) + 2 < ref_llf:
				print('*******************************')
				print('len AP-REF %s' % str(ref_llf))
				print('len AP-N %s' % str(len(ap.params['associatedStations'])))
				print('len AP-N +2 %s' % str(len(ap.params['associatedStations']) + 2))
				print('len AP-N compar %s' % str(len(ap.params['associatedStations']) + 2 < ref_llf))
				debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
				sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
				self.changeAP = True
		else:
			self.changeAP = True
		return self.changeAP

	def ssf(self, sta, ap, wlan, ap_wlan):
		#ssf: Strongest signal first
		tiempo_inicial = time.time()
		distance = sta.get_distance_to(sta.params['associatedTo'][wlan])
		rssi = sta.get_rssi(sta.params['associatedTo'][wlan],
							wlan, distance)
		ref_dist = sta.get_distance_to(ap)
		ref_rssi = sta.get_rssi(ap, wlan, ref_dist)
		if float(ref_rssi) > float(rssi + 0.1):
			tiempo_final = time.time()
			time_selec = tiempo_final - tiempo_inicial
			debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
			sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
			self.changeAP = True
			print("**************************method execution**************************")
			f= open("/home/mininet/Escritorio/scripts/output/ssf.txt","a+")
			f.write('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(ap.name), str(sta.params['apsInRange']), str(sta.params['battery']), str(sta.params['position'])))
			f.close()
			print('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(ap.name), str(sta.params['apsInRange']), str(sta.params['battery']), str(sta.params['position'])))
			sta.params['battery'] = sta.params['battery'] - 0.1
			#print("assoc_py node: %s - battery: %s" % (sta.name, str(sta.params['battery'])))
		return self.changeAP

	def ssf2(self, sta, ap, wlan, ap_wlan):
		#ssf: Strongest signal first
		distance = sta.get_distance_to(sta.params['associatedTo'][wlan])
		rssi = sta.get_rssi(sta.params['associatedTo'][wlan],
							wlan, distance)
		ref_dist = sta.get_distance_to(ap)
		ref_rssi = sta.get_rssi(ap, wlan, ref_dist)
		#f_handover = open("/home/mininet/Escritorio/scripts/output/f_hanfover.txt","a")
		print("Comparison - Custom association method")
		print("AP_REF %s" % sta.params['associatedTo'][wlan])
		print("AP_N %s" %ap.params['ssid'])
		print("RSSI_REF %s" % ref_rssi)
		print("RSSI_N %s" % str(float(rssi)))
		print("RSSI_N + 0.1 %s" % str(float(rssi + 0.1)))
		print("RSSI_N COMP %s" % str(float(ref_rssi) > float(rssi + 0.1)))
		
		if float(ref_rssi) > float(rssi + 0.1):
			debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
			sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
			self.changeAP = True
			milliseconds = int(round(time.time() * 1000))
			#f_handover.write('Time start handover %s \n' %milliseconds)
			#f_handover.write('Handover SSF %s \n \n' % sta.params['wlan'][wlan])
			print("----------------------Custom association method----------------------")
			print("RSSI_REF %s" % ref_rssi)
			print("RSSI_N %s" % str(float(rssi)))
			print("RSSI_N + 0.1 %s" % str(float(rssi + 0.1)))
			print("RSSI_N COMP %s" % str(float(ref_rssi) > float(rssi + 0.1)))
			
			print("Custom association method")
			print(milliseconds)
			print('Time start handover' + time.strftime("%H:%M:%S") )
			print('Handover SSF %s' % sta.params['wlan'][wlan])
		#f_handover.close()
		return self.changeAP

	def slf(self, sta, ap, wlan, ap_wlan):
		#slf: Custom association method
		tiempo_inicial = time.time()
		#ssf params
		distance = sta.get_distance_to(sta.params['associatedTo'][wlan])
		rssi = sta.get_rssi(sta.params['associatedTo'][wlan], wlan, distance)
		ref_dist = sta.get_distance_to(ap)
		ref_rssi = sta.get_rssi(ap, wlan, ref_dist)
		
		#llf params
		apref = sta.params['associatedTo'][wlan]
		
		if apref != '':
			if float(ref_rssi) > float(rssi + 0.1):
				ref_llf = len(apref.params['associatedStations'])
				if len(ap.params['associatedStations']) + 2 < ref_llf:
					tiempo_final = time.time()
					time_selec = tiempo_final - tiempo_inicial
					debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
					sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
					print("**************************method execution**************************")
					f= open("/home/mininet/Escritorio/scripts/output/slf.txt","a+")
					#f.write('{"time":"%s","sta":"%s","oldAp":"%s", "newAp":"%s", "apsInRange":"%s","battery":"%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(ap.name), str(sta.params['apsInRange']), str(sta.params['battery'])))
					print('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(ap.name), str(sta.params['apsInRange']), str(sta.params['battery']), str(sta.params['position'])))
					f.write('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(ap.name), str(sta.params['apsInRange']), str(sta.params['battery']), str(sta.params['position'])))
					f.close()
					sta.params['battery'] = sta.params['battery'] - 0.1
					#print("assoc_py node: %s - battery: %s" % (sta.name, str(sta.params['battery'])))
					self.changeAP = True
		else:
			self.changeAP = True
		return self.changeAP
		

	def slf2(self, sta, ap, wlan, ap_wlan):
		#slf: Custom association method
		
		#ssf params
		distance = sta.get_distance_to(sta.params['associatedTo'][wlan])
		rssi = sta.get_rssi(sta.params['associatedTo'][wlan], wlan, distance)
		ref_dist = sta.get_distance_to(ap)
		ref_rssi = sta.get_rssi(ap, wlan, ref_dist)
		
		#llf params
		apref = sta.params['associatedTo'][wlan]
		
		
		print("\nComparison - Custom association method")
		
		print("AP_REF %s" % sta.params['associatedTo'][wlan])
		print("AP_N %s" %ap.params['ssid'])
		
		print("SSF")

		print("RSSI_REF %s" % ref_rssi)
		print("RSSI_N %s" % str(float(rssi)))
		print("RSSI_N + 0.1 %s" % str(float(rssi + 0.1)))
		print("RSSI_N COMP %s" % str(float(ref_rssi) > float(rssi + 0.1)))
		
		print("LLF")
		print('len AP-N %s' % str(len(ap.params['associatedStations'])))
		print('len AP-N +2 %s' % str(len(ap.params['associatedStations']) + 2))
		print('len AP-N compar %s' % str(len(ap.params['associatedStations']) + 2 < len(apref.params['associatedStations']) ))
		
		print('comparisons')
		print("RSSI_N COMP %s" % str(float(ref_rssi) > float(rssi + 0.1)))
		print('len AP-N compar %s' % str(len(ap.params['associatedStations']) + 2 < len(apref.params['associatedStations']) ))
		
		if apref != '':
			if float(ref_rssi) > float(rssi + 0.1):
				ref_llf = len(apref.params['associatedStations'])
				if len(ap.params['associatedStations']) + 2 < ref_llf:
					debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
					sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
					print("**************************method execution**************************")
					print("\nComparison - Custom association method")
					
					print("AP_REF %s" % sta.params['associatedTo'][wlan])
					print("AP_N %s" %ap.params['ssid'])
					
					print("\nSSF")

					print("RSSI_REF %s" % ref_rssi)
					print("RSSI_N %s" % str(float(rssi)))
					print("RSSI_N + 0.1 %s" % str(float(rssi + 0.1)))
					print("RSSI_N COMP %s" % str(float(ref_rssi) > float(rssi + 0.1)))
					
					print("\nLLF")
					print('len AP-N %s' % str(len(ap.params['associatedStations'])))
					print('len AP-N +2 %s' % str(len(ap.params['associatedStations']) + 2))
					print('len AP-N compar %s' % str(len(ap.params['associatedStations']) + 2 < len(apref.params['associatedStations']) ))
					
					print('\ncomparisons')
					print("RSSI_N COMP %s" % str(float(ref_rssi) > float(rssi + 0.1)))
					print('len AP-N compar %s' % str(len(ap.params['associatedStations']) + 2 < len(apref.params['associatedStations']) ))
					print("**************************End - method execution**************************")
					self.changeAP = True
		else:
			self.changeAP = True
		return self.changeAP
	
	def topsis(self, sta, ap, wlan, ap_wlan):
		#topsis_VFinal_CON_GRUPOS contiene la implementacion final de topsis JUNTO CON la implementacion de movilidad en grupo
		#TOPSIS: Technique for Order of Preference by Similarity to Ideal Solution (sin movilidad en grupo)
		print("\n---TOPSIS CON GRUPOS---")
		tiempo_inicial = time.time() 
		"""
		aps = ""
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps = aps + ap_temp2.name[2:]
		"""
		ap_names = ["ap1","ap2","ap3","ap4"]
		ind = False
		ind_group = False
		info_group =[]
		
		list_rf = []
		list_rf2 = []
		
		#Inicio Movilidad en grupo
		id_group = sta.params.get("id_group", "null")
		aps_posible =[]
		
		num_dis_group = 1
		ind_AP_selection = False
		#TOPSIS
		md = np.array([])						#MATRIZ DE DECISION
		mp = np.array([ 0.33, 0.36, 0.31])
		Alist = [r for r in md]
		aps_temp = []

		if id_group =="null":
			print('ac--Station sin grupo')
			print('ac--Station hace la asociacion normal')
			print("ac--name station: ", str(sta.name))
			print("ac-- aqui va la parte del segundo escaneo__escaneo para guardar la info de los aps cuando NO estan agrupados")
			print("ac-- segundo escaneo - al final se elimina")
			for i in range( len(sta.params["apsInRange"]) ):
				ap_temp = sta.params['apsInRange'][i]
				# RSSI
				rssi_aptemp = sta.get_rssi(ap_temp,0,sta.get_distance_to(ap_temp))
				
				if str(ap_temp.name) == str(sta.params['associatedTo'][wlan]):
					n_est_aptemp = len(ap_temp.params['associatedStations'])
				else:
					n_est_aptemp = len(ap_temp.params['associatedStations']) + 2
				
				dis_to_aptemp = sta.get_distance_to(ap_temp)
				
				#bat_temp = 0.01 * dis_to_aptemp
				
				sta_app = sta.params.get("app", 1)
				# BATERIA
				bat_temp = 0.001 * dis_to_aptemp * sta_app
				
				print("ap: " + str(ap_temp.name) + " distancia: " + str(dis_to_aptemp) + " app: " + str(sta_app) + " bat_temp" + str(bat_temp))
				
				#n_est_aptemp = len(ap_temp.params['associatedStations'])
				#dis_to_aptemp = sta.get_distance_to(ap_temp)
				"""
				print ("AP name %s" %ap_temp.name )
				print ("RSSI %s" %str(rssi_aptemp) )
				print ("# estations %s" %str(n_est_aptemp) )
				print ("Distance to AP %s" %str(dis_to_aptemp) )
				"""
				#newrow = [ap_temp.name, rssi_aptemp, n_est_aptemp, dis_to_aptemp]
				#newrow = [rssi_aptemp, n_est_aptemp*-1, dis_to_aptemp*1000]
				#newrow = [rssi_aptemp, n_est_aptemp*-1, dis_to_aptemp*-1]
				# OCUPACION
				ocup_aptemp = (n_est_aptemp*100.)/ap_temp.params['maxDis'] # se saca la ocupacion del AP en porcentaje
				#print("num_sta: " + str(n_est_aptemp)+ " - max_disp: " + str(ap_temp.params['maxDis']) +  " - ocupacion: " + str(ocup_aptemp))
				#newrow = [rssi_aptemp*-1, n_est_aptemp, bat_temp]
				newrow = [rssi_aptemp*-1, ocup_aptemp, bat_temp]
				Alist.append(newrow)
				aps_temp.append(ap_temp.name)
			md = np.array(Alist)
			print("---------Array a predecir---------")
			print(md)
			ind_AP_selection = True
			ind_group = False
			#print(sta.params['apsInRange'])
			
		else:
			print('ac--Station con grupo')
			print('ac--Se busca el lider del grupo')
			print("ac--name: ", str(sta.name))
			leader_name = gm.group_leader_info(id_group)
			
			print("ac--name station: ", str(sta.name))
			print("ac--name leader: ", str(leader_name))
			
			info_group = gm.group_info(id_group)
			bw_group = info_group["bw"]
			num_dis_group = len(info_group["disp"])
			
			print("ac--info_grupo: ", str(info_group))
			#print("ac--type_info_group: ", str(type(info_group)))
			print("ac--info_group_lider: ", str(leader_name))
			print("ac--info_group_stations: ", str(info_group["disp"]))
			print("ac--info_group_bw: ", str(bw_group))
			
			"""
			# start DISPOSITIVOS QUE CONFORMAN EL GRUPO (estos son los dispositivos que tienen que pasar al nuevo AP de ser necesario)
			print("ac--info_group_disp_data: ", str(info_group["disp_data"]))
			
			for disp in info_group["disp_data"]:
				print("ac--info_group_disp_data_disp: ", str(disp))
				print("ac--info_group_disp_data_position: ", str(disp.params['position']))
				print("ac--info_group_disp_data_type: ", str(type(disp)))
			# end DISPOSITIVOS QUE CONFORMAN EL GRUPO
			"""
			
			if (sta.name == leader_name):
				print('ac--lider y stacion son iguales')
				print('ac--Se hace la asociacion para el grupo')
				
				aps_in_range_name = []
				rssi_aps_in_range = []
				bw_aps_in_range=[]
				bw_aps_in_range_minus_bw_group=[]
				bw_aps_in_range_minus_bw_connected_devices=[]
				
				
				for n in range( len(sta.params["apsInRange"]) ):
					ap_temp_n = sta.params['apsInRange'][n]
					aps_in_range_name.append(ap_temp_n.name)
					
					rssi_ap_temp_n = sta.get_rssi(ap_temp_n,0,sta.get_distance_to(ap_temp_n))
					rssi_aps_in_range.append(rssi_ap_temp_n)
					
					bw_ap_temp_n = ap_temp_n.params['bw_ap']
					bw_aps_in_range.append(bw_ap_temp_n)
					#aps = aps + ap_temp2.name[2:]
					
					bw_ap_temp_n_ninus_bw_group = bw_ap_temp_n - bw_group
					bw_aps_in_range_minus_bw_group.append(bw_ap_temp_n_ninus_bw_group) 
					
					"""
					if ap_temp_n == ap_conectado:
						# no restar el bw del grupo
						#bw = bw_total_ap-bw_consumo_actual
					else:
						#restar el bw del grupo
						#bw = bw_total_ap-bw_consumo_actual-bw_grupo
					"""
					bw_connected_devices = 0
					for i in range( len(ap_temp_n.params["associatedStations"]) ):
						sta_ap_temp = ap_temp_n.params["associatedStations"][i]
						bw_sta_ap_temp = sta_ap_temp.params["bw_d"]
						print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", sta_ap_temp: ", str(sta_ap_temp.name), ", bw_sta_ap_temp: ", str(bw_sta_ap_temp))
						bw_connected_devices = bw_connected_devices + bw_sta_ap_temp
					print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_connected_devices: ", str(bw_connected_devices))
					
					bw_total = 0
					#if ap_temp_name == str(sta.params['associatedTo'][wlan]):
					
					print("ac--ap_temp_n.name: ", str(ap_temp_n.name))
					print("ac--ap_associatedTo: ", str(sta.params['associatedTo'][wlan]))
					
					if str(ap_temp_n.name) == str(sta.params['associatedTo'][wlan]):
						#bw_ap_temp_n_nimus_bw_connected_devices
						# no restar el bw del grupo
						bw_total = bw_ap_temp_n-bw_connected_devices
						print("ac--ap_temp_n == ap_associatedTo")
						print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_ap_temp_n: ", str(bw_ap_temp_n))
						print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_connected_devices: ", str(bw_connected_devices))
						#bw = bw_total_ap-bw_consumo_actual
					else:
						#restar el bw del grupo
						#bw = bw_total_ap-bw_consumo_actual-bw_grupo
						bw_total = bw_ap_temp_n-bw_connected_devices-bw_group
						print("ac--ap_temp_n != ap_associatedTo")
						print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_ap_temp_n: ", str(bw_ap_temp_n))
						print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_connected_devices: ", str(bw_connected_devices))
						print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_group: ", str(bw_group))
						
						
					#bw_ap_temp_n_minus_bw_conected_device = bw_ap_temp_n_minus_bw_conected_device - bw_sta_ap_temp
					
					print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_total: ", str(bw_total))
					#bw_aps_in_range_minus_bw_connected_devices
					
					
					if bw_total <= 0:
						#no se guarda
						print("ac--NO se guarda el ap, el bw es menor a cero")
					else:
						#se se guarda(posible ap a elegir)
						print("ac--SI se guarda el ap, el bw es mayor a cero")
						aps_posible.append(ap_temp_n.name)
					
					print("ac--*********")
					
				print("ac--name_aps_in_range", str(aps_in_range_name))
				print("ac--rssi_aps_in_range", str(rssi_aps_in_range))
				print("ac--bw_aps_in_range", str(bw_aps_in_range))
				#print("ac--bw_aps_in_range_minus_bw_group", str(bw_aps_in_range_minus_bw_group))
				print("ac--aps_posible", str(aps_posible))
				
				print("ac-- aqui va la parte del primer escaneo__escaneo para guardar la info de los aps cuando estan agrupados")
				
				
				print("ac-- inicio primer escaneo - al final se deja")
				for i in range(len(ap_names)):
					for i2 in range( len(sta.params["apsInRange"]) ):
						ap_temp = sta.params['apsInRange'][i2]
						ap_temp_name = str(ap_temp.name)
						
						if (ap_names[i] ==  ap_temp_name) and (ap_temp_name in aps_posible):
							print("ac--SI guarda los datos reales del ap: ", str(ap_temp_name))
							
							print("ac--num disp del grupo: ",str(num_dis_group))
							
							# RSSI
							ap_temp_dis = sta.get_distance_to(ap_temp) # distancia del adispositivo al AP
							ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  #RSSI del dispositivo al AP
							"""
							if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
								ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  # RSSI del dispositivo al AP se mantiene
							else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
								ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis) #RSSI del dispositivo al AP se le resta 2
							"""
							
							
							# BATERIA
							sta_app = sta.params.get("app", 1) #Se saca que aplicacion (ninguna-1, voz-2, audio-3, video-4) corre el dispositivo
							ap_temp_con = 0.001 * ap_temp_dis * sta_app #consumo de bateria (depende de la distancia y la aplicacion del dispositivo)
							#print("ap: " + str(ap_temp.name) + " distancia: " + str(ap_temp_dis) + " app: " + str(sta_app) + " bat_temp" + str(ap_temp_con))
							"""
							if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
								ap_temp_con = 0.001 * ap_temp_dis * sta_app  # RSSI del dispositivo al AP se mantiene
							else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
								ap_temp_con = (0.001 * ap_temp_dis * sta_app)  #RSSI del dispositivo al AP se le resta 2
							"""
							print("ac-- ap_temp",str(ap_temp_name))
							print("ac-- ap_asociado",str(sta.params['associatedTo'][wlan]))
							print("ac-- disp conectados",str(len(ap_temp.params['associatedStations'])))
							print("ac-- max disp conectados",str(ap_temp.params['maxDis']))
							
							
							# OCUPACION
							if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
								ap_temp_num_sta = len(ap_temp.params['associatedStations']) # el numero de dispositivos se mantiene
							else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
								ap_temp_num_sta = len(ap_temp.params['associatedStations']) + 2 + num_dis_group # al numero de dispositivos se le aumenta 2
							#ap_temp_num_sta = len(ap_temp.params['associatedStations'])
							
							ap_temp_ocu = ((ap_temp_num_sta*100.)/ap_temp.params['maxDis']) # se saca la ocupacion del AP en porcentaje
							
							# Escribir datos en dataset
							#f_datos_entrenamiento.write("{},{},{},{:.4f},".format(str(ap_temp.name), str(ap_temp_rssi), str(ap_temp_ocu),ap_temp_con))
							
							#f_datos_entrenamiento.write("{},{},{},{:.4f},".format("1", str(ap_temp_rssi), str(ap_temp_ocu), ap_temp_con))
							
							newrow = [ap_temp_rssi*-1, ap_temp_ocu, ap_temp_con]
							Alist.append(newrow)
							aps_temp.append(ap_temp.name)
							#temp_list_rf = [1, ap_temp_rssi, ap_temp_ocu, ap_temp_con]
							
							#list_rf.extend(temp_list_rf)
							#print("ac-- ap a guardar con datos reales", str(temp_list_rf))
							
							ind = True
							break
						else:
							ind = False
						
					if ind == False:
						#temp_list_rf = [0, -100.0, 100, 1.0]
						#list_rf.extend(temp_list_rf)
						print("ac-- el ap no se guarda")
						#f_datos_entrenamiento.write("{},{},{},{},".format("0", "xx", "yy","zz"))
				md = np.array(Alist)
				print("---------Array final a predecir---------")
				print(md)
				#solution = pred([list_rf])
				#ap_n = "ap{}".format(solution[0])
				print("ac-- fin primer escaneo - al final se deja")
				ind_AP_selection = True
				ind_group = True
				
			else:
				print('ac--lider y estacion son diferentes')
				print('ac--se pasa a la siguiente estacion')
				print('ac--esta estacion no realiza la asociacion')
				ind_AP_selection = False
				ind_group = True
			#Fin Movilidad en grupo
			
		if ind_AP_selection == True: # Es verdadero cuando hay un dipositivo sin grupo o cuando el que esta realizando la solicitu es el lider
			
			print('inicio seleccion de AP')
			print('list_rf FINAL')
			print(md)
			
			m21 = 1./md
		
			m22 = m21**2
			
			m23 = m22.sum(axis=0)
			
			m24 = m23**(0.5)
			
			mnd = m21/m24
			
			#matriz normalizada de pesos
			mnp = mnd * mp
			
			#maximos y minimos de cada columna
			v_max = mnp.max(axis=0)
			v_min = mnp.min(axis=0)
			
			#Calcular la separacion de la SOLUCION IDEAL POSITIVA Y NEGATIVA (PIS)(NIS) 
			
			#PIS
			m41 = mnp - v_max
			m42 = m41**2
			m_pis = m42.sum(axis=1)**(0.5) 

			#NIS
			m412 = mnp - v_min
			m422 = m412**2
			m_nis = m422.sum(axis=1)**(0.5) 
			
			
			m_sep = np.array([m_pis,m_nis])		#MATRIZ de separacion a la SOLUCION IDEAL
			
			# cercania relativa a la solucion ideal
			m51 = m_sep.sum(axis=0)
			
			v_cer = m_sep[1,0:]/m51
			solution = aps_temp[v_cer.argmax()]
			ap_n = solution

			#solution = pred([list_rf])
			#ap_n = "ap{}".format(solution[0])
			
			aps_in_range_name = []
			rssi_aps_in_range = []
			for n in range( len(sta.params["apsInRange"]) ):
				ap_temp2 = sta.params['apsInRange'][n]
				aps_in_range_name.append(ap_temp2.name)
				
				rssi_aptemp = sta.get_rssi(ap_temp2,0,sta.get_distance_to(ap_temp2))
				rssi_aps_in_range.append(rssi_aptemp)
				
				#aps = aps + ap_temp2.name[2:]
			
			print("aps en rango")
			print(aps_in_range_name)
			
			print("RSSI aps en rango")
			print(rssi_aps_in_range)
			
			print("aps seleccionado")
			print(ap_n)
			
			hist = sta.params.get("hist", "null")

			if ap_n in aps_in_range_name:
				if str(sta.params['associatedTo'][wlan]) != str(ap_n):
					tiempo_final = time.time()
					time_selec = tiempo_final - tiempo_inicial
					f= open("/home/mininet/Escritorio/scripts/output/topsis.txt","a+")
					if ind_group == False: #No esta agrupado
						f.write("2_inicio del cambio el ap al que esta conectado ya no esta en rango\n")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("2_fin del cambio\n")
						print ("2_CAMBIO.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						
					else:#Se va a hacer el cambio a un grupo de dispositivos
						# start DISPOSITIVOS QUE CONFORMAN EL GRUPO (estos son los dispositivos que tienen que pasar al nuevo AP de ser necesario)
						
						print("ac--info_group_disp_data: ", str(info_group["disp_data"]))
						
						aps_range_sta = sta.params['apsInRange']
						all_in_range = False
						for disp in info_group["disp_data"]:
							aps_range_temp = disp.params['apsInRange']
							comp = set(aps_range_sta).intersection(aps_range_temp)
							print("ac--info_group_2_sta_aps_in_range: ", str(sta), str(aps_range_sta))
							print("ac--info_group_2_disp_aps_in_range: ", str(disp), str(aps_range_temp))
							print("ac--info_group_2_comp: ", str(comp))
							print("ac--info_group_2_len: ", str(len(comp)))
							if len(comp) == len(sta.params['apsInRange']):
								all_in_range = True
							else:
								all_in_range = False
						
						if all_in_range == True:
							for disp in info_group["disp_data"]:
								print("ac--info_group_2_disp_data_disp: ", str(disp))
								print("ac--info_group_2_disp_data_position: ", str(disp.params['position']))
								print("ac--info_group_2_disp_data_type: ", str(type(disp)))
								f.write("ac--info_group_2_inicio del cambio el ap al que esta conectado ya no esta en rango\n")
									
								indice = aps_in_range_name.index(str(ap_n))
								
								print("ac--info_group_2_disp_[indice]: ", str(indice))
								print("ac--info_group_2_disp.params['apsInRange'][indice]: ", str(disp.params['apsInRange']))
								print("ac--info_group_2_disp.params_aps_in_range_name: ", str(aps_in_range_name))
								print("ac--info_group_2_disp.params_ap_n: ", str(ap_n))
								
								
								f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(disp.name),str(disp.params['associatedTo'][wlan]), str(disp.params['apsInRange'][indice]), str(aps_in_range_name), str(disp.params['battery']), str(disp.params['position'])))
								f.write("ac--info_group_2_fin del cambio\n")
								print ("ac--info_group_2_CAMBIO.................................................................................")
								debug('iw dev %s disconnect\n' % disp.params['wlan'][wlan])
								disp.pexec('iw dev %s disconnect' % disp.params['wlan'][wlan])
								Association.associate_infra(disp, disp.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
								disp.params['battery'] = disp.params['battery'] - 0.1
								# end DISPOSITIVOS QUE CONFORMAN EL GRUPO
						else:
							print("ac-- no todos los dispositivos estan en rango")
						
					print("2_SI SE REALIZA EL CAMBIO")
					
					
					f.close()
				else:
					print("2_NO SE REALIZA EL CAMBIO - misma red")	
			else:
				print('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
		else:
			print('estacion no realiza seleccion de AP')
		return self.changeAP
		
	
	def topsis_VFinal_SIN_Grupos(self, sta, ap, wlan, ap_wlan):
		#topsis_VFinal_SIN_Grupos contiene la implementacion final de topsis sin la implementacion de movilidad en grupo
		#TOPSIS: Technique for Order of Preference by Similarity to Ideal Solution (sin movilidad en grupo)
		#print("\n---TOPSIS Normalizacion por costo---")
		print("\n---TOPSIS SIN GRUPOS---")
		tiempo_inicial = time.time() 
		md = np.array([])						#MATRIZ DE DECISION
		#mp = np.array([ 2./6, 1./6, 3./6])		#VECTOR DE PESOS
		#mp = np.array([ 2./5., 2./5., 1./5.])
		#mp = np.array([ 0.3, 0.5, 0.2])
		#mp = np.array([ 0.5, 0.5, 0.0])
		#mp = np.array([ 1/3, 1/3, 1/3])
		#mp = np.array([ 0.0, 0.0, 1.0])
		#mp = np.array([ 0.2, 0.5, 0.3])
		#mp = np.array([ 0.2974, 0.6167, 0.0859])
		mp = np.array([ 0.33, 0.36, 0.31])
		Alist = [r for r in md]
		aps_temp = []
		
		for i in range( len(sta.params["apsInRange"]) ):
			ap_temp = sta.params['apsInRange'][i]
			rssi_aptemp = sta.get_rssi(ap_temp,0,sta.get_distance_to(ap_temp))
			
			if str(ap_temp.name) == str(sta.params['associatedTo'][wlan]):
				n_est_aptemp = len(ap_temp.params['associatedStations'])
			else:
				n_est_aptemp = len(ap_temp.params['associatedStations']) + 2
			
			dis_to_aptemp = sta.get_distance_to(ap_temp)
			
			#bat_temp = 0.01 * dis_to_aptemp
			
			sta_app = sta.params.get("app", 1)
			
			bat_temp = 0.001 * dis_to_aptemp * sta_app
			
			print("ap: " + str(ap_temp.name) + " distancia: " + str(dis_to_aptemp) + " app: " + str(sta_app) + " bat_temp" + str(bat_temp))
			
			#n_est_aptemp = len(ap_temp.params['associatedStations'])
			#dis_to_aptemp = sta.get_distance_to(ap_temp)
			"""
			print ("AP name %s" %ap_temp.name )
			print ("RSSI %s" %str(rssi_aptemp) )
			print ("# estations %s" %str(n_est_aptemp) )
			print ("Distance to AP %s" %str(dis_to_aptemp) )
			"""
			#newrow = [ap_temp.name, rssi_aptemp, n_est_aptemp, dis_to_aptemp]
			#newrow = [rssi_aptemp, n_est_aptemp*-1, dis_to_aptemp*1000]
			#newrow = [rssi_aptemp, n_est_aptemp*-1, dis_to_aptemp*-1]
			
			ocup_aptemp = (n_est_aptemp*100.)/ap_temp.params['maxDis'] # se saca la ocupacion del AP en porcentaje
			#print("num_sta: " + str(n_est_aptemp)+ " - max_disp: " + str(ap_temp.params['maxDis']) +  " - ocupacion: " + str(ocup_aptemp))
			#newrow = [rssi_aptemp*-1, n_est_aptemp, bat_temp]
			newrow = [rssi_aptemp*-1, ocup_aptemp, bat_temp]
			Alist.append(newrow)
			aps_temp.append(ap_temp.name)
		
		md = np.array(Alist)
		"""
		print(aps_temp)
		print(md)
		print(mp)
		"""
		
		"""
		md12 = md**2
		md13 = md12.sum(axis=0)**(0.5)	#divisor de cada columna
		
		#matriz normalizada de decision
		mnd = md/md13
		"""
		
		m21 = 1./md
		
		m22 = m21**2
		
		m23 = m22.sum(axis=0)
		
		m24 = m23**(0.5)
		
		mnd = m21/m24
		
		#matriz normalizada de pesos
		mnp = mnd * mp
		
		#maximos y minimos de cada columna
		v_max = mnp.max(axis=0)
		v_min = mnp.min(axis=0)
		
		#Calcular la separacion de la SOLUCION IDEAL POSITIVA Y NEGATIVA (PIS)(NIS) 
		
		#PIS
		m41 = mnp - v_max
		m42 = m41**2
		m_pis = m42.sum(axis=1)**(0.5) 

		#NIS
		m412 = mnp - v_min
		m422 = m412**2
		m_nis = m422.sum(axis=1)**(0.5) 
		
		
		m_sep = np.array([m_pis,m_nis])		#MATRIZ de separacion a la SOLUCION IDEAL
		
		# cercania relativa a la solucion ideal
		m51 = m_sep.sum(axis=0)
		
		v_cer = m_sep[1,0:]/m51
		"""
		print('vector de cercanias')
		print(v_cer)
		#mejor red
		print('mejor red')
		print(v_cer.max())
		#Posicion del argumento maximo
		print('posicion de la mejor red')
		print(v_cer.argmax())
		"""
		"""
		f_prueba= open("/home/mininet/Escritorio/scripts/output/topsis_prueba.txt","a+")
		f_prueba.write("%s\n" %md)
		f_prueba.close()
		
		f_prueba2= open("/home/mininet/Escritorio/scripts/output/topsis_prueba2.txt","a+")
		f_prueba2.write("%s %s %s %s\n" %(str(sta.name), aps_temp, str(sta.params['associatedTo'][wlan]), str(sta.params['position'])))
		f_prueba2.close()
		"""
		if str(sta.params['associatedTo'][wlan]) != aps_temp[v_cer.argmax()]:
			tiempo_final = time.time()
			time_selec = tiempo_final - tiempo_inicial
			f= open("/home/mininet/Escritorio/scripts/output/topsis.txt","a+")
			print('diferente red')
			print("**************************method execution**************************")
			"""
			print('\n---------------------------------------')
			print('Old AP: ' + str(sta.params['associatedTo'][wlan]))
			print('New AP: ' + str(sta.params['apsInRange'][v_cer.argmax()].name))
			print('New AP2: ' + str(aps_temp[v_cer.argmax()]))
			print('New AP: ' + str(sta.params['apsInRange']))
			"""
			#f.write('\n\n---------------------------------------')
			#f.write('\nOld AP: ' + str(sta.params['associatedTo'][wlan]))
			#f.write('\nNew AP: ' + str(aps_temp[v_cer.argmax()]))
			#f.write('\nAps in Range: ' + str(sta.params['apsInRange']))
			#f.write("{}, {}, {}\n".format(str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp)))
			#f.write("oldAp:'%s', newAp:'%s', apsInRange:'%s'\n" %(str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp)))
			#print('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp), str(sta.params['battery']), str(sta.params['position'])))
			f.write('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp), str(sta.params['battery']), str(sta.params['position'])))
			#f.write('{"time":"%s", "sta":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s", "oldAp":"%s", "newAp":"%s"}\n' %(str(time_selec*1000),str(sta.name), str(aps_temp), str(sta.params['battery']), str(sta.params['position']), str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()])))
			#f.write(str(sta.params['associatedTo'][wlan]))
			f.close()
			debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
			sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
			Association.associate_infra(sta, sta.params['apsInRange'][v_cer.argmax()], wlan=wlan, ap_wlan=ap_wlan)
			sta.params['battery'] = sta.params['battery'] - 0.1
			#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
			#print("assoc_py node: %s - battery: %s" % (sta.name, str(sta.params['battery'])))
			
		else:
			print('misma red')
			
		return self.changeAP

	def topsis2(self, sta, ap, wlan, ap_wlan):
		#TOPSIS: Technique for Order of Preference by Similarity to Ideal Solution
		#print("\n---TOPSIS Normalizacion por beneficio---")
		tiempo_inicial = time.time() 
		md = np.array([])						#MATRIZ DE DECISION
		#mp = np.array([ 2./6, 1./6, 3./6])		#VECTOR DE PESOS
		#mp = np.array([ 2./5., 2./5., 1./5.])
		mp = np.array([ 0.6, 0.4])
		Alist = [r for r in md]
		aps_temp = []
		
		for i in range( len(sta.params["apsInRange"]) ):
			ap_temp = sta.params['apsInRange'][i]
			rssi_aptemp = sta.get_rssi(ap_temp,0,sta.get_distance_to(ap_temp))
			
			if str(ap_temp.name) == str(sta.params['associatedTo'][wlan]):
				n_est_aptemp = len(ap_temp.params['associatedStations'])
			else:
				n_est_aptemp = len(ap_temp.params['associatedStations']) + 2
			
			#n_est_aptemp = len(ap_temp.params['associatedStations'])
			#dis_to_aptemp = sta.get_distance_to(ap_temp)
			"""
			print ("AP name %s" %ap_temp.name )
			print ("RSSI %s" %str(rssi_aptemp) )
			print ("# estations %s" %str(n_est_aptemp) )
			print ("Distance to AP %s" %str(dis_to_aptemp) )
			"""
			#newrow = [ap_temp.name, rssi_aptemp, n_est_aptemp, dis_to_aptemp]
			#newrow = [rssi_aptemp, n_est_aptemp*-1, dis_to_aptemp*1000]
			#newrow = [rssi_aptemp, n_est_aptemp*-1, dis_to_aptemp*-1]
			newrow = [rssi_aptemp, n_est_aptemp*-1]
			Alist.append(newrow)
			aps_temp.append(ap_temp.name)
		
		md = np.array(Alist)
		
		print(aps_temp)
		print(md)
		print(mp)
		
		md12 = md**2
		md13 = md12.sum(axis=0)**(0.5)	#divisor de cada columna
		
		#matriz normalizada de decision
		mnd = md/md13
		
		#matriz normalizada de pesos
		mnp = mnd * mp
		
		#maximos y minimos de cada columna
		v_max = mnp.max(axis=0)
		v_min = mnp.min(axis=0)
		
		#Calcular la separacion de la SOLUCION IDEAL POSITIVA Y NEGATIVA (PIS)(NIS) 
		
		#PIS
		m41 = mnp - v_max
		m42 = m41**2
		m_pis = m42.sum(axis=1)**(0.5) 

		#NIS
		m412 = mnp - v_min
		m422 = m412**2
		m_nis = m422.sum(axis=1)**(0.5) 
		
		
		m_sep = np.array([m_pis,m_nis])		#MATRIZ de separacion a la SOLUCION IDEAL
		
		# cercania relativa a la solucion ideal
		m51 = m_sep.sum(axis=0)
		
		v_cer = m_sep[1,0:]/m51
		"""
		print('vector de cercanias')
		print(v_cer)
		#mejor red
		print('mejor red')
		print(v_cer.max())
		#Posicion del argumento maximo
		print('posicion de la mejor red')
		print(v_cer.argmax())
		"""
		if str(sta.params['associatedTo'][wlan]) != aps_temp[v_cer.argmax()]:
			tiempo_final = time.time()
			time_selec = tiempo_final - tiempo_inicial
			f= open("/home/mininet/Escritorio/scripts/output/topsis.txt","a+")
			print('diferente red')
			print("**************************method execution**************************")
			"""
			print('\n---------------------------------------')
			print('Old AP: ' + str(sta.params['associatedTo'][wlan]))
			print('New AP: ' + str(sta.params['apsInRange'][v_cer.argmax()].name))
			print('New AP2: ' + str(aps_temp[v_cer.argmax()]))
			print('New AP: ' + str(sta.params['apsInRange']))
			"""
			#f.write('\n\n---------------------------------------')
			#f.write('\nOld AP: ' + str(sta.params['associatedTo'][wlan]))
			#f.write('\nNew AP: ' + str(aps_temp[v_cer.argmax()]))
			#f.write('\nAps in Range: ' + str(sta.params['apsInRange']))
			#f.write("{}, {}, {}\n".format(str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp)))
			#f.write("oldAp:'%s', newAp:'%s', apsInRange:'%s'\n" %(str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp)))
			#print('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp), str(sta.params['battery']), str(sta.params['position'])))
			f.write('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp), str(sta.params['battery']), str(sta.params['position'])))
			#f.write('{"time":"%s", "sta":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s", "oldAp":"%s", "newAp":"%s"}\n' %(str(time_selec*1000),str(sta.name), str(aps_temp), str(sta.params['battery']), str(sta.params['position']), str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()])))
			#f.write(str(sta.params['associatedTo'][wlan]))
			f.close()
			debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
			sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
			Association.associate_infra(sta, sta.params['apsInRange'][v_cer.argmax()], wlan=wlan, ap_wlan=ap_wlan)
			sta.params['battery'] = sta.params['battery'] - 0.1
			#print("assoc_py node: %s - battery: %s" % (sta.name, str(sta.params['battery'])))
			
		else:
			print('misma red')
			
		return self.changeAP

	def topsis3(self, sta, ap, wlan, ap_wlan):
		#TOPSIS: Technique for Order of Preference by Similarity to Ideal Solution
		#print("\n---TOPSIS---")
		tiempo_inicial = time.time() 
		md = np.array([])						#MATRIZ DE DECISION
		#mp = np.array([ 2./6, 1./6, 3./6])		#VECTOR DE PESOS
		mp = np.array([ 2./5., 2./5., 1./5.])
		Alist = [r for r in md]
		aps_temp = []
		
		for i in range( len(sta.params["apsInRange"]) ):
			ap_temp = sta.params['apsInRange'][i]
			rssi_aptemp = sta.get_rssi(ap_temp,0,sta.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta.get_distance_to(ap_temp)
			"""
			print ("AP name %s" %ap_temp.name )
			print ("RSSI %s" %str(rssi_aptemp) )
			print ("# estations %s" %str(n_est_aptemp) )
			print ("Distance to AP %s" %str(dis_to_aptemp) )
			"""
			#newrow = [ap_temp.name, rssi_aptemp, n_est_aptemp, dis_to_aptemp]
			#newrow = [rssi_aptemp, n_est_aptemp*-1, dis_to_aptemp*1000]
			newrow = [rssi_aptemp, n_est_aptemp*-1, dis_to_aptemp*-1]
			Alist.append(newrow)
			aps_temp.append(ap_temp.name)
		
		md = np.array(Alist)
		"""
		print(aps_temp)
		print(md)
		print(mp)
		"""
		md12 = md**2
		md13 = md12.sum(axis=0)**(0.5)	#divisor de cada columna
		
		#matriz normalizada de decision
		mnd = md/md13
		
		#matriz normalizada de pesos
		mnp = mnd * mp
		
		#maximos y minimos de cada columna
		v_max = mnp.max(axis=0)
		v_min = mnp.min(axis=0)
		
		#Calcular la separacion de la SOLUCION IDEAL POSITIVA Y NEGATIVA (PIS)(NIS) 
		
		#PIS
		m41 = mnp - v_max
		m42 = m41**2
		m_pis = m42.sum(axis=1)**(0.5) 

		#NIS
		m412 = mnp - v_min
		m422 = m412**2
		m_nis = m422.sum(axis=1)**(0.5) 
		
		
		m_sep = np.array([m_pis,m_nis])		#MATRIZ de separacion a la SOLUCION IDEAL
		
		# cercania relativa a la solucion ideal
		m51 = m_sep.sum(axis=0)
		
		v_cer = m_sep[1,0:]/m51
		"""
		print('vector de cercanias')
		print(v_cer)
		#mejor red
		print('mejor red')
		print(v_cer.max())
		#Posicion del argumento maximo
		print('posicion de la mejor red')
		print(v_cer.argmax())
		"""
		if str(sta.params['associatedTo'][wlan]) != aps_temp[v_cer.argmax()]:
			tiempo_final = time.time()
			time_selec = tiempo_final - tiempo_inicial
			f= open("/home/mininet/Escritorio/scripts/output/topsis.txt","a+")
			print('diferente red')
			print("**************************method execution**************************")
			"""
			print('\n---------------------------------------')
			print('Old AP: ' + str(sta.params['associatedTo'][wlan]))
			print('New AP: ' + str(sta.params['apsInRange'][v_cer.argmax()].name))
			print('New AP2: ' + str(aps_temp[v_cer.argmax()]))
			print('New AP: ' + str(sta.params['apsInRange']))
			"""
			#f.write('\n\n---------------------------------------')
			#f.write('\nOld AP: ' + str(sta.params['associatedTo'][wlan]))
			#f.write('\nNew AP: ' + str(aps_temp[v_cer.argmax()]))
			#f.write('\nAps in Range: ' + str(sta.params['apsInRange']))
			#f.write("{}, {}, {}\n".format(str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp)))
			#f.write("oldAp:'%s', newAp:'%s', apsInRange:'%s'\n" %(str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp)))
			#print('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp), str(sta.params['battery']), str(sta.params['position'])))
			f.write('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp), str(sta.params['battery']), str(sta.params['position'])))
			#f.write('{"time":"%s", "sta":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s", "oldAp":"%s", "newAp":"%s"}\n' %(str(time_selec*1000),str(sta.name), str(aps_temp), str(sta.params['battery']), str(sta.params['position']), str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()])))
			#f.write(str(sta.params['associatedTo'][wlan]))
			f.close()
			debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
			sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
			Association.associate_infra(sta, sta.params['apsInRange'][v_cer.argmax()], wlan=wlan, ap_wlan=ap_wlan)
			sta.params['battery'] = sta.params['battery'] - 0.1
			#print("assoc_py node: %s - battery: %s" % (sta.name, str(sta.params['battery'])))
			
		else:
			print('misma red')
			
		return self.changeAP


	def saw(self, sta, ap, wlan, ap_wlan):
		#SAW: Simple Additive Weighting
		print("\n---SAW---")
		tiempo_inicial = time.time() 
		md = np.array([])						#MATRIZ DE DECISION
		#mp = np.array([ 2./6, 1./6, 3./6])		#VECTOR DE PESOS
		#mp = np.array([ 2./5., 2./5., 1./5.])
		#mp = np.array([ 0.4, 0.6])
		mp = np.array([ 0.33, 0.36, 0.31])
		Alist = [r for r in md]
		aps_temp = []
		
		for i in range( len(sta.params["apsInRange"]) ):
			ap_temp = sta.params['apsInRange'][i]
			rssi_aptemp = sta.get_rssi(ap_temp,0,sta.get_distance_to(ap_temp))
			#n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta.get_distance_to(ap_temp)
			if str(ap_temp.name) == str(sta.params['associatedTo'][wlan]):
				n_est_aptemp = len(ap_temp.params['associatedStations'])
			else:
				n_est_aptemp = len(ap_temp.params['associatedStations']) + 2
			
			dis_to_aptemp = sta.get_distance_to(ap_temp)
			
			sta_app = sta.params.get("app", 1)
			
			bat_temp = 0.001 * dis_to_aptemp * sta_app
			
			print("ap: " + str(ap_temp.name) + " distancia: " + str(dis_to_aptemp) + " app: " + str(sta_app) + " bat_temp" + str(bat_temp))
			
			
			"""
			print ("AP name %s" %ap_temp.name )
			print ("RSSI %s" %str(rssi_aptemp) )
			print ("# estations %s" %str(n_est_aptemp) )
			print ("Distance to AP %s" %str(dis_to_aptemp) )
			"""
			
			#newrow = [ap_temp.name, rssi_aptemp, n_est_aptemp, dis_to_aptemp]
			#newrow = [rssi_aptemp, n_est_aptemp*-1, dis_to_aptemp*1000]
			#newrow = [rssi_aptemp*-1, n_est_aptemp, dis_to_aptemp]
			
			ocup_aptemp = (n_est_aptemp*100.)/ap_temp.params['maxDis'] # se saca la ocupacion del AP en porcentaje
			
			
			print("num_sta: " + str(n_est_aptemp)+ " - max_disp: " + str(ap_temp.params['maxDis']) +  " - ocupacion: " + str(ocup_aptemp))
			#print("application: " + str(sta_app))
			
			newrow = [rssi_aptemp*-1, ocup_aptemp, bat_temp]
			#newrow = [rssi_aptemp*-1, n_est_aptemp, bat_temp]
			Alist.append(newrow)
			aps_temp.append(ap_temp.name)
			n2_est_aptemp = len(ap_temp.params['associatedStations'])
			f= open("/home/mininet/Escritorio/scripts/output/datosML3.txt","a+")
			f.write("{},{},{},{},{},{},{}\n".format(str(sta.name), str(ap_temp.name), str(rssi_aptemp), str(n2_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta.params['associatedTo'][wlan])))
			f.close()
		
		md = np.array(Alist)
		"""
		print(aps_temp)
		print(md)
		print(mp)
		"""
		#maximos de cada columna de la matriz de decision
		m2 = md.min(axis=0)
		#print ("max")
		#print m2
		#matriz de decision sobre el vector de maximos
		m3 = m2/md
		#print ("m3")
		#print m3
		
		# multiplicar por el vector de pesos
		m4 = m3 * mp
		#print ("m4")
		#print m4
		
		#suma de las filas (vector de cercanias)
		v_cer = m4.sum(axis=1)
		#print ("m5")
		#print v_cer
		
		#mejor red
		#print ("mejor red puntaje")
		#print(v_cer.max())
		#Posicion del argumento maximo
		#print ("mejor red posicion")
		#print(v_cer.argmax())
		
		
		if str(sta.params['associatedTo'][wlan]) != aps_temp[v_cer.argmax()]:
			tiempo_final = time.time()
			time_selec = tiempo_final - tiempo_inicial
			f= open("/home/mininet/Escritorio/scripts/output/saw.txt","a+")
			"""
			print('diferente red')
			print("**************************method execution**************************")
			print ("aps")
			print(aps_temp)
			print ("matriz decision")
			print(md)
			print ("vector pesos")
			print(mp)
			print ("vector cercanias")
			print v_cer
			print ("mejor red puntaje")
			print(v_cer.max())
			#Posicion del argumento maximo
			print ("mejor red posicion")
			print(v_cer.argmax())
			"""
			
			"""
			print('\n---------------------------------------')
			print('Old AP: ' + str(sta.params['associatedTo'][wlan]))
			print('New AP: ' + str(sta.params['apsInRange'][v_cer.argmax()].name))
			print('New AP2: ' + str(aps_temp[v_cer.argmax()]))
			print('New AP: ' + str(sta.params['apsInRange']))
			"""
			#f.write('\n\n---------------------------------------')
			#f.write('\nOld AP: ' + str(sta.params['associatedTo'][wlan]))
			#f.write('\nNew AP: ' + str(aps_temp[v_cer.argmax()]))
			#f.write('\nAps in Range: ' + str(sta.params['apsInRange']))
			#f.write("{}, {}, {}\n".format(str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp)))
			#f.write("oldAp:'%s', newAp:'%s', apsInRange:'%s'\n" %(str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp)))
			#print('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp), str(sta.params['battery']), str(sta.params['position'])))
			f.write('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp), str(sta.params['battery']), str(sta.params['position'])))
			#f.write('{"time":"%s", "sta":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s", "oldAp":"%s", "newAp":"%s"}\n' %(str(time_selec*1000),str(sta.name), str(aps_temp), str(sta.params['battery']), str(sta.params['position']), str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()])))
			f.close()
			debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
			sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
			Association.associate_infra(sta, sta.params['apsInRange'][v_cer.argmax()], wlan=wlan, ap_wlan=ap_wlan)
			sta.params['battery'] = sta.params['battery'] - 0.1
			#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
			#print("assoc_py node: %s - battery: %s" % (sta.name, str(sta.params['battery'])))
			
		else:
			print('misma red')
		
		return self.changeAP

	def saw2(self, sta, ap, wlan, ap_wlan):
		#SAW: Simple Additive Weighting
		print("\n---SAW---")
		tiempo_inicial = time.time() 
		md = np.array([])						#MATRIZ DE DECISION
		#mp = np.array([ 2./6, 1./6, 3./6])		#VECTOR DE PESOS
		mp = np.array([ 2./5., 2./5., 1./5.])
		Alist = [r for r in md]
		aps_temp = []
		
		for i in range( len(sta.params["apsInRange"]) ):
			ap_temp = sta.params['apsInRange'][i]
			rssi_aptemp = sta.get_rssi(ap_temp,0,sta.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta.get_distance_to(ap_temp)
			"""
			print ("AP name %s" %ap_temp.name )
			print ("RSSI %s" %str(rssi_aptemp) )
			print ("# estations %s" %str(n_est_aptemp) )
			print ("Distance to AP %s" %str(dis_to_aptemp) )
			"""
			#newrow = [ap_temp.name, rssi_aptemp, n_est_aptemp, dis_to_aptemp]
			#newrow = [rssi_aptemp, n_est_aptemp*-1, dis_to_aptemp*1000]
			newrow = [rssi_aptemp*-1, n_est_aptemp, dis_to_aptemp]
			Alist.append(newrow)
			aps_temp.append(ap_temp.name)
		
		md = np.array(Alist)
		"""
		print(aps_temp)
		print(md)
		print(mp)
		"""
		#maximos de cada columna de la matriz de decision
		m2 = md.min(axis=0)
		#print ("max")
		#print m2
		#matriz de decision sobre el vector de maximos
		m3 = m2/md
		#print ("m3")
		#print m3
		
		# multiplicar por el vector de pesos
		m4 = m3 * mp
		#print ("m4")
		#print m4
		
		#suma de las filas (vector de cercanias)
		v_cer = m4.sum(axis=1)
		#print ("m5")
		#print v_cer
		
		#mejor red
		#print ("mejor red puntaje")
		#print(v_cer.max())
		#Posicion del argumento maximo
		#print ("mejor red posicion")
		#print(v_cer.argmax())
		
		
		if str(sta.params['associatedTo'][wlan]) != aps_temp[v_cer.argmax()]:
			tiempo_final = time.time()
			time_selec = tiempo_final - tiempo_inicial
			f= open("/home/mininet/Escritorio/scripts/output/saw.txt","a+")
			print('diferente red')
			print("**************************method execution**************************")
			print ("aps")
			print(aps_temp)
			print ("matriz decision")
			print(md)
			print ("vector pesos")
			print(mp)
			print ("vector cercanias")
			print v_cer
			print ("mejor red puntaje")
			print(v_cer.max())
			#Posicion del argumento maximo
			print ("mejor red posicion")
			print(v_cer.argmax())
			"""
			print('\n---------------------------------------')
			print('Old AP: ' + str(sta.params['associatedTo'][wlan]))
			print('New AP: ' + str(sta.params['apsInRange'][v_cer.argmax()].name))
			print('New AP2: ' + str(aps_temp[v_cer.argmax()]))
			print('New AP: ' + str(sta.params['apsInRange']))
			"""
			#f.write('\n\n---------------------------------------')
			#f.write('\nOld AP: ' + str(sta.params['associatedTo'][wlan]))
			#f.write('\nNew AP: ' + str(aps_temp[v_cer.argmax()]))
			#f.write('\nAps in Range: ' + str(sta.params['apsInRange']))
			#f.write("{}, {}, {}\n".format(str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp)))
			#f.write("oldAp:'%s', newAp:'%s', apsInRange:'%s'\n" %(str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp)))
			#print('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp), str(sta.params['battery']), str(sta.params['position'])))
			f.write('{"time":"%s", "sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()]), str(aps_temp), str(sta.params['battery']), str(sta.params['position'])))
			#f.write('{"time":"%s", "sta":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s", "oldAp":"%s", "newAp":"%s"}\n' %(str(time_selec*1000),str(sta.name), str(aps_temp), str(sta.params['battery']), str(sta.params['position']), str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()])))
			f.close()
			debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
			sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
			Association.associate_infra(sta, sta.params['apsInRange'][v_cer.argmax()], wlan=wlan, ap_wlan=ap_wlan)
			sta.params['battery'] = sta.params['battery'] - 0.1
			#print("assoc_py node: %s - battery: %s" % (sta.name, str(sta.params['battery'])))
			
		else:
			print('misma red')
		
		return self.changeAP

	def rf_V4_1__prueba__no_funciona(self, sta, ap, wlan, ap_wlan):
		#RF: Random Forest
		print("\n---RF---")
		tiempo_inicial = time.time() 
		"""
		aps = ""
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps = aps + ap_temp2.name[2:]
		"""
		ap_names = ["ap1","ap2","ap3","ap4"]
		ind = False
		
		list_rf = []
		
		for i in range(len(ap_names)):
			for i2 in range( len(sta.params["apsInRange"]) ):
				ap_temp = sta.params['apsInRange'][i2]
				ap_temp_name = str(ap_temp.name)
				
				if ap_names[i] == ap_temp_name:
					
					# RSSI
					ap_temp_dis = sta.get_distance_to(ap_temp) # distancia del adispositivo al AP
					ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  #RSSI del dispositivo al AP
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis) #RSSI del dispositivo al AP se le resta 2
					"""
					
					
					# BATERIA
					sta_app = sta.params.get("app", 1) #Se saca que aplicacion (ninguna-1, voz-2, audio-3, video-4) corre el dispositivo
					ap_temp_con = 0.001 * ap_temp_dis * sta_app #consumo de bateria (depende de la distancia y la aplicacion del dispositivo)
					#print("ap: " + str(ap_temp.name) + " distancia: " + str(ap_temp_dis) + " app: " + str(sta_app) + " bat_temp" + str(ap_temp_con))
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_con = 0.001 * ap_temp_dis * sta_app  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_con = (0.001 * ap_temp_dis * sta_app)  #RSSI del dispositivo al AP se le resta 2
					"""
					
					# OCUPACION
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) # el numero de dispositivos se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) + 2 # al numero de dispositivos se le aumenta 2
					#ap_temp_num_sta = len(ap_temp.params['associatedStations'])
					
					ap_temp_ocu = ((ap_temp_num_sta*100.)/ap_temp.params['maxDis']) # se saca la ocupacion del AP en porcentaje
					
					# Escribir datos en dataset
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format(str(ap_temp.name), str(ap_temp_rssi), str(ap_temp_ocu),ap_temp_con))
					
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format("1", str(ap_temp_rssi), str(ap_temp_ocu), ap_temp_con))
					
					temp_list_rf = [1, ap_temp_rssi, ap_temp_ocu, ap_temp_con]
					
					list_rf.extend(temp_list_rf)
					
					ind = True
					break
				else:
					ind = False
				
			if ind == False:
				temp_list_rf = [0, -100.0, 100, 1.0]
				list_rf.extend(temp_list_rf)
				#f_datos_entrenamiento.write("{},{},{},{},".format("0", "xx", "yy","zz"))
		print("---------Array a predecir---------")
		print(list_rf)
		solution = pred([list_rf])
		ap_n = "ap{}".format(solution[0])
		
		aps_in_range_name = []
		rssi_aps_in_range = []
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps_in_range_name.append(ap_temp2.name)
			
			rssi_aptemp = sta.get_rssi(ap_temp2,0,sta.get_distance_to(ap_temp2))
			rssi_aps_in_range.append(rssi_aptemp)
			
			#aps = aps + ap_temp2.name[2:]
		
		print("aps en rango")
		print(aps_in_range_name)
		
		print("RSSI aps en rango")
		print(rssi_aps_in_range)
		
		print("aps seleccionado")
		print(ap_n)
		
		
		#indice = aps_in_range_rssi.index(max(aps_in_range_rssi))
		rssi_max = max(rssi_aps_in_range)
		n=0
		
		ap_candidates_rssi = []
		
		for rssi_ap in rssi_aps_in_range:
			if rssi_max == rssi_ap:
				#print n
				print(rssi_aps_in_range[n])
				print(aps_in_range_name[n])
				ap_candidates_rssi.append(aps_in_range_name[n])
				#print (i)
			n = n+1
		print(ap_candidates_rssi)
		
		if ap_n in aps_in_range_name:
			if str(sta.params['associatedTo'][wlan]) != str(ap_n):
				if str(sta.params['associatedTo'][wlan]) in aps_in_range_name:
					print("El ap al que esta asociado si esta en rango\n")
					if sta.params['rssi'][0] != rssi_max:
						print("El ap al que esta asociado no tiene el mayor RSSI\n")
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						f.write("inicio del cambio el ap al qu esta conectado aun esta en rango")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("fin del cambio")
						print ("CAMBIO.................................................................................")
						print ("CAMBIO.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
						"""
						if ap_n in ap_candidates_rssi:
							print("El ap nuevo esta entre los ap candidatos por el rssi\n")
							tiempo_final = time.time()
							time_selec = tiempo_final - tiempo_inicial
							f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
							f.write("inicio del cambio el ap al qu esta conectado aun esta en rango")
							indice = aps_in_range_name.index(str(ap_n))
							f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
							f.write("fin del cambio")
							print ("CAMBIO.................................................................................")
							print ("CAMBIO.................................................................................")
							debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
							sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
							Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
							sta.params['battery'] = sta.params['battery'] - 0.1
							#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
							f.close()
						"""
					else:
						#print('El ap nuevo NO esta entre los ap candidatos')
						print('El ap al que esta asociado no tiene el mayor RSSI')
						
						
				else:
					print("El ap al que esta asociado NO esta en rango\n")
					tiempo_final = time.time()
					time_selec = tiempo_final - tiempo_inicial
					f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
					f.write("inicio del cambio el ap al que esta conectado ya no esta en rango\n")
					indice = aps_in_range_name.index(str(ap_n))
					f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
					f.write("fin del cambio\n")
					print ("CAMBIO.................................................................................")
					print ("CAMBIO.................................................................................")
					debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
					sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
					Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
					sta.params['battery'] = sta.params['battery'] - 0.1
					#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
					f.close()
			else:
				#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
				print('misma red')
		#if ap_n in aps_temp:
		else:
			print('*******AP NOOOO ESTA EN RANGO*******')
			#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
			#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
		
		"""
		if ap_n in aps_in_range_name:
			#f_2.write("****{},{}\n".format(aps_temp,ap_n))
			if str(sta.params['associatedTo'][wlan]) != str(ap_n):
				tiempo_final = time.time()
				time_selec = tiempo_final - tiempo_inicial
				
				#f_2.write("**************************************SI Cambio de AP{}-------------------------\n".format(mode[0][0]))
				#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
				#f_2.write("ap_n: {}, array_indice: {}, array_ap: {}, ap: {}\n".format(ap_n, indice, aps_temp[indice], sta.params['apsInRange'][indice]))
				#f_2.write("-------------------------\n")
				
				#print("El AP - {} esta en la posicion {} de la lista".format(ap_n,indice))
				indice = aps_in_range_name.index(str(ap_n))
				f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
				#f.write("{},{},{}\n".format(sta.name, str(sta.params['associatedTo'][wlan]),mrf))
				f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
				#f.write('{"time":"%s", "sta":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s", "oldAp":"%s", "newAp":"%s"}\n' %(str(time_selec*1000),str(sta.name), str(aps_temp), str(sta.params['battery']), str(sta.params['position']), str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()])))
				debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
				sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
				Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
				sta.params['battery'] = sta.params['battery'] - 0.1
				#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
				f.close()
			else:
				#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
				print('misma red')
		#if ap_n in aps_temp:
		else:
			print('*******AP NOOOO ESTA EN RANGO*******')
			#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
			#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
		"""
		return self.changeAP
		

	def rf(self, sta, ap, wlan, ap_wlan):
		#rf_V5_3_CON_Group_movility_V1_0: Random Forest final con este se elimina el efecti ping pong de RF_V2_0 y se implementa la movilidad en grupo
		print("\n---RF---")
		tiempo_inicial = time.time() 
		"""
		aps = ""
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps = aps + ap_temp2.name[2:]
		"""
		ap_names = ["ap1","ap2","ap3","ap4"]
		ind = False
		ind_group = False
		info_group =[]
		
		list_rf = []
		list_rf2 = []
		
		#Inicio Movilidad en grupo
		id_group = sta.params.get("id_group", "null")
		aps_posible =[]
		
		num_dis_group = 1
		ind_AP_selection = False
		if id_group =="null":
			print('ac--Station sin grupo')
			print('ac--Station hace la asociacion normal')
			print("ac--name station: ", str(sta.name))
			print("ac-- aqui va la parte del segundo escaneo__escaneo para guardar la info de los aps cuando NO estan agrupados")
			print("ac-- segundo escaneo - al final se elimina")
			for i in range(len(ap_names)):
				for i2 in range( len(sta.params["apsInRange"]) ):
					ap_temp = sta.params['apsInRange'][i2]
					ap_temp_name = str(ap_temp.name)
					
					if ap_names[i] == ap_temp_name:
						
						# RSSI
						ap_temp_dis = sta.get_distance_to(ap_temp) # distancia del adispositivo al AP
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  #RSSI del dispositivo al AP
						"""
						if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
							ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  # RSSI del dispositivo al AP se mantiene
						else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
							ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis) #RSSI del dispositivo al AP se le resta 2
						"""
						
						
						# BATERIA
						sta_app = sta.params.get("app", 1) #Se saca que aplicacion (ninguna-1, voz-2, audio-3, video-4) corre el dispositivo
						ap_temp_con = 0.001 * ap_temp_dis * sta_app #consumo de bateria (depende de la distancia y la aplicacion del dispositivo)
						#print("ap: " + str(ap_temp.name) + " distancia: " + str(ap_temp_dis) + " app: " + str(sta_app) + " bat_temp" + str(ap_temp_con))
						"""
						if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
							ap_temp_con = 0.001 * ap_temp_dis * sta_app  # RSSI del dispositivo al AP se mantiene
						else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
							ap_temp_con = (0.001 * ap_temp_dis * sta_app)  #RSSI del dispositivo al AP se le resta 2
						"""
						
						# OCUPACION
						if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
							ap_temp_num_sta = len(ap_temp.params['associatedStations']) # el numero de dispositivos se mantiene
						else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
							ap_temp_num_sta = len(ap_temp.params['associatedStations']) + 2 # al numero de dispositivos se le aumenta 2
						#ap_temp_num_sta = len(ap_temp.params['associatedStations'])
						
						ap_temp_ocu = ((ap_temp_num_sta*100.)/ap_temp.params['maxDis']) # se saca la ocupacion del AP en porcentaje
						
						# Escribir datos en dataset
						#f_datos_entrenamiento.write("{},{},{},{:.4f},".format(str(ap_temp.name), str(ap_temp_rssi), str(ap_temp_ocu),ap_temp_con))
						
						#f_datos_entrenamiento.write("{},{},{},{:.4f},".format("1", str(ap_temp_rssi), str(ap_temp_ocu), ap_temp_con))
						
						temp_list_rf = [1, ap_temp_rssi, ap_temp_ocu, ap_temp_con]
						
						list_rf.extend(temp_list_rf)
						
						ind = True
						break
					else:
						ind = False
					
				if ind == False:
					temp_list_rf = [0, -100.0, 100, 1.0]
					list_rf.extend(temp_list_rf)
					#f_datos_entrenamiento.write("{},{},{},{},".format("0", "xx", "yy","zz"))
			print("---------Array a predecir---------")
			print(list_rf)
			ind_AP_selection = True
			ind_group = False
			#print(sta.params['apsInRange'])
			
		else:
			print('ac--Station con grupo')
			print('ac--Se busca el lider del grupo')
			print("ac--name: ", str(sta.name))
			leader_name = gm.group_leader_info(id_group)
			
			print("ac--name station: ", str(sta.name))
			print("ac--name leader: ", str(leader_name))
			
			info_group = gm.group_info(id_group)
			bw_group = info_group["bw"]
			num_dis_group = len(info_group["disp"])
			
			print("ac--info_grupo: ", str(info_group))
			#print("ac--type_info_group: ", str(type(info_group)))
			print("ac--info_group_lider: ", str(leader_name))
			print("ac--info_group_stations: ", str(info_group["disp"]))
			print("ac--info_group_bw: ", str(bw_group))
			
			"""
			# start DISPOSITIVOS QUE CONFORMAN EL GRUPO (estos son los dispositivos que tienen que pasar al nuevo AP de ser necesario)
			print("ac--info_group_disp_data: ", str(info_group["disp_data"]))
			
			for disp in info_group["disp_data"]:
				print("ac--info_group_disp_data_disp: ", str(disp))
				print("ac--info_group_disp_data_position: ", str(disp.params['position']))
				print("ac--info_group_disp_data_type: ", str(type(disp)))
			# end DISPOSITIVOS QUE CONFORMAN EL GRUPO
			"""
			
			if (sta.name == leader_name):
				print('ac--lider y stacion son iguales')
				print('ac--Se hace la asociacion para el grupo')
				
				aps_in_range_name = []
				rssi_aps_in_range = []
				bw_aps_in_range=[]
				bw_aps_in_range_minus_bw_group=[]
				bw_aps_in_range_minus_bw_connected_devices=[]
				
				
				for n in range( len(sta.params["apsInRange"]) ):
					ap_temp_n = sta.params['apsInRange'][n]
					aps_in_range_name.append(ap_temp_n.name)
					
					rssi_ap_temp_n = sta.get_rssi(ap_temp_n,0,sta.get_distance_to(ap_temp_n))
					rssi_aps_in_range.append(rssi_ap_temp_n)
					
					bw_ap_temp_n = ap_temp_n.params['bw_ap']
					bw_aps_in_range.append(bw_ap_temp_n)
					#aps = aps + ap_temp2.name[2:]
					
					bw_ap_temp_n_ninus_bw_group = bw_ap_temp_n - bw_group
					bw_aps_in_range_minus_bw_group.append(bw_ap_temp_n_ninus_bw_group) 
					
					"""
					if ap_temp_n == ap_conectado:
						# no restar el bw del grupo
						#bw = bw_total_ap-bw_consumo_actual
					else:
						#restar el bw del grupo
						#bw = bw_total_ap-bw_consumo_actual-bw_grupo
					"""
					bw_connected_devices = 0
					for i in range( len(ap_temp_n.params["associatedStations"]) ):
						sta_ap_temp = ap_temp_n.params["associatedStations"][i]
						bw_sta_ap_temp = sta_ap_temp.params["bw_d"]
						print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", sta_ap_temp: ", str(sta_ap_temp.name), ", bw_sta_ap_temp: ", str(bw_sta_ap_temp))
						bw_connected_devices = bw_connected_devices + bw_sta_ap_temp
					print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_connected_devices: ", str(bw_connected_devices))
					
					bw_total = 0
					#if ap_temp_name == str(sta.params['associatedTo'][wlan]):
					
					print("ac--ap_temp_n.name: ", str(ap_temp_n.name))
					print("ac--ap_associatedTo: ", str(sta.params['associatedTo'][wlan]))
					
					if str(ap_temp_n.name) == str(sta.params['associatedTo'][wlan]):
						#bw_ap_temp_n_nimus_bw_connected_devices
						# no restar el bw del grupo
						bw_total = bw_ap_temp_n-bw_connected_devices
						print("ac--ap_temp_n == ap_associatedTo")
						print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_ap_temp_n: ", str(bw_ap_temp_n))
						print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_connected_devices: ", str(bw_connected_devices))
						#bw = bw_total_ap-bw_consumo_actual
					else:
						#restar el bw del grupo
						#bw = bw_total_ap-bw_consumo_actual-bw_grupo
						bw_total = bw_ap_temp_n-bw_connected_devices-bw_group
						print("ac--ap_temp_n != ap_associatedTo")
						print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_ap_temp_n: ", str(bw_ap_temp_n))
						print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_connected_devices: ", str(bw_connected_devices))
						print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_group: ", str(bw_group))
						
						
					#bw_ap_temp_n_minus_bw_conected_device = bw_ap_temp_n_minus_bw_conected_device - bw_sta_ap_temp
					
					print("ac--ap_temp_n.name: ", str(ap_temp_n.name), ", bw_total: ", str(bw_total))
					#bw_aps_in_range_minus_bw_connected_devices
					
					
					if bw_total <= 0:
						#no se guarda
						print("ac--NO se guarda el ap, el bw es menor a cero")
					else:
						#se se guarda(posible ap a elegir)
						print("ac--SI se guarda el ap, el bw es mayor a cero")
						aps_posible.append(ap_temp_n.name)
					
					print("ac--*********")
					
				print("ac--name_aps_in_range", str(aps_in_range_name))
				print("ac--rssi_aps_in_range", str(rssi_aps_in_range))
				print("ac--bw_aps_in_range", str(bw_aps_in_range))
				#print("ac--bw_aps_in_range_minus_bw_group", str(bw_aps_in_range_minus_bw_group))
				print("ac--aps_posible", str(aps_posible))
				
				print("ac-- aqui va la parte del primer escaneo__escaneo para guardar la info de los aps cuando estan agrupados")
				
				
				print("ac-- inicio primer escaneo - al final se deja")
				for i in range(len(ap_names)):
					for i2 in range( len(sta.params["apsInRange"]) ):
						ap_temp = sta.params['apsInRange'][i2]
						ap_temp_name = str(ap_temp.name)
						
						if (ap_names[i] ==  ap_temp_name) and (ap_temp_name in aps_posible):
							print("ac--SI guarda los datos reales del ap: ", str(ap_temp_name))
							
							print("ac--num disp del grupo: ",str(num_dis_group))
							
							# RSSI
							ap_temp_dis = sta.get_distance_to(ap_temp) # distancia del adispositivo al AP
							ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  #RSSI del dispositivo al AP
							"""
							if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
								ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  # RSSI del dispositivo al AP se mantiene
							else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
								ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis) #RSSI del dispositivo al AP se le resta 2
							"""
							
							
							# BATERIA
							sta_app = sta.params.get("app", 1) #Se saca que aplicacion (ninguna-1, voz-2, audio-3, video-4) corre el dispositivo
							ap_temp_con = 0.001 * ap_temp_dis * sta_app #consumo de bateria (depende de la distancia y la aplicacion del dispositivo)
							#print("ap: " + str(ap_temp.name) + " distancia: " + str(ap_temp_dis) + " app: " + str(sta_app) + " bat_temp" + str(ap_temp_con))
							"""
							if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
								ap_temp_con = 0.001 * ap_temp_dis * sta_app  # RSSI del dispositivo al AP se mantiene
							else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
								ap_temp_con = (0.001 * ap_temp_dis * sta_app)  #RSSI del dispositivo al AP se le resta 2
							"""
							print("ac-- ap_temp",str(ap_temp_name))
							print("ac-- ap_asociado",str(sta.params['associatedTo'][wlan]))
							print("ac-- disp conectados",str(len(ap_temp.params['associatedStations'])))
							print("ac-- max disp conectados",str(ap_temp.params['maxDis']))
							
							
							# OCUPACION
							if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
								ap_temp_num_sta = len(ap_temp.params['associatedStations']) # el numero de dispositivos se mantiene
							else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
								ap_temp_num_sta = len(ap_temp.params['associatedStations']) + 2 + num_dis_group # al numero de dispositivos se le aumenta 2
							#ap_temp_num_sta = len(ap_temp.params['associatedStations'])
							
							ap_temp_ocu = ((ap_temp_num_sta*100.)/ap_temp.params['maxDis']) # se saca la ocupacion del AP en porcentaje
							
							# Escribir datos en dataset
							#f_datos_entrenamiento.write("{},{},{},{:.4f},".format(str(ap_temp.name), str(ap_temp_rssi), str(ap_temp_ocu),ap_temp_con))
							
							#f_datos_entrenamiento.write("{},{},{},{:.4f},".format("1", str(ap_temp_rssi), str(ap_temp_ocu), ap_temp_con))
							
							temp_list_rf = [1, ap_temp_rssi, ap_temp_ocu, ap_temp_con]
							
							list_rf.extend(temp_list_rf)
							print("ac-- ap a guardar con datos reales", str(temp_list_rf))
							
							ind = True
							break
						else:
							ind = False
						
					if ind == False:
						temp_list_rf = [0, -100.0, 100, 1.0]
						list_rf.extend(temp_list_rf)
						#f_datos_entrenamiento.write("{},{},{},{},".format("0", "xx", "yy","zz"))
				print("---------Array final a predecir---------")
				print(list_rf)
				#solution = pred([list_rf])
				#ap_n = "ap{}".format(solution[0])
				print("ac-- fin primer escaneo - al final se deja")
				ind_AP_selection = True
				ind_group = True
				
			else:
				print('ac--lider y stacion son diferentes')
				print('ac--se pasa a la siguiente estacion')
				print('ac--esta estacion no realiza la asociacion')
				ind_AP_selection = False
				ind_group = True
			#Fin Movilidad en grupo
			
		if ind_AP_selection == True: # Es verdadero cuando hay un dipositivo sin grupo o cuando el que esta realizando la solicitud es el lider
			
			print('inicio seleccion de AP')
			print('list_rf FINAL')
			print(list_rf)
			solution = pred([list_rf])
			ap_n = "ap{}".format(solution[0])
			
			aps_in_range_name = []
			rssi_aps_in_range = []
			for n in range( len(sta.params["apsInRange"]) ):
				ap_temp2 = sta.params['apsInRange'][n]
				aps_in_range_name.append(ap_temp2.name)
				
				rssi_aptemp = sta.get_rssi(ap_temp2,0,sta.get_distance_to(ap_temp2))
				rssi_aps_in_range.append(rssi_aptemp)
				
				#aps = aps + ap_temp2.name[2:]
			
			print("aps en rango")
			print(aps_in_range_name)
			
			print("RSSI aps en rango")
			print(rssi_aps_in_range)
			
			print("aps seleccionado")
			print(ap_n)
			
			hist = sta.params.get("hist", "null")
			
			if hist != "null":
				print("2_ SI tiene hist")
				if ap_n in aps_in_range_name:
					print("2_ AP predicho SI esta entre los aps en rango")
					hist_scan = hist[3] # se saca el historial de aps_predichos
					ap_ejm = hist_scan[0] # se saca del historial un ap para comparar con los demas
					print(ap_ejm)
					mode = 1
					for i in hist_scan[1:]: #ciclo para escanear todo el historial de aps_predichos
						if ap_ejm == i: #condicion para comparar los aps 
							mode = mode+1
						else: 
							break #si no son iguales se rompe el ciclo
					print(hist_scan)
					print("mode = " + str(mode))
					
					if mode == 6: # 14 es el normal si el historial de aps predichos son todos iguales se pasa a la siguiente etapa
						print("--La moda es igual")
						if str(sta.params['associatedTo'][wlan]) != str(ap_n):
							tiempo_final = time.time()
							time_selec = tiempo_final - tiempo_inicial
							f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
							if ind_group == False: #No esta agrupado
								f.write("2_inicio del cambio el ap al que esta conectado ya no esta en rango\n")
								indice = aps_in_range_name.index(str(ap_n))
								f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
								f.write("2_fin del cambio\n")
								print ("2_CAMBIO.................................................................................")
								debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
								sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
								Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
								sta.params['battery'] = sta.params['battery'] - 0.1
								#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
								
							else:#Se va a hacer el cambio a un grupo de dispositivos
								# start DISPOSITIVOS QUE CONFORMAN EL GRUPO (estos son los dispositivos que tienen que pasar al nuevo AP de ser necesario)
								
								print("ac--info_group_disp_data: ", str(info_group["disp_data"]))
								
								aps_range_sta = sta.params['apsInRange']
								all_in_range = False
								for disp in info_group["disp_data"]:
									aps_range_temp = disp.params['apsInRange']
									comp = set(aps_range_sta).intersection(aps_range_temp)
									print("ac--info_group_2_sta_aps_in_range: ", str(sta), str(aps_range_sta))
									print("ac--info_group_2_disp_aps_in_range: ", str(disp), str(aps_range_temp))
									print("ac--info_group_2_comp: ", str(comp))
									print("ac--info_group_2_len: ", str(len(comp)))
									if len(comp) == len(sta.params['apsInRange']):
										all_in_range = True
									else:
										all_in_range = False
								
								if all_in_range == True:
									for disp in info_group["disp_data"]:
										print("ac--info_group_2_disp_data_disp: ", str(disp))
										print("ac--info_group_2_disp_data_position: ", str(disp.params['position']))
										print("ac--info_group_2_disp_data_type: ", str(type(disp)))
										f.write("ac--info_group_2_inicio del cambio el ap al que esta conectado ya no esta en rango\n")
										 
										indice = aps_in_range_name.index(str(ap_n))
										
										print("ac--info_group_2_disp_[indice]: ", str(indice))
										print("ac--info_group_2_disp.params['apsInRange'][indice]: ", str(disp.params['apsInRange']))
										print("ac--info_group_2_disp.params_aps_in_range_name: ", str(aps_in_range_name))
										print("ac--info_group_2_disp.params_ap_n: ", str(ap_n))
										
										
										f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(disp.name),str(disp.params['associatedTo'][wlan]), str(disp.params['apsInRange'][indice]), str(aps_in_range_name), str(disp.params['battery']), str(disp.params['position'])))
										f.write("ac--info_group_2_fin del cambio\n")
										print ("ac--info_group_2_CAMBIO.................................................................................")
										debug('iw dev %s disconnect\n' % disp.params['wlan'][wlan])
										disp.pexec('iw dev %s disconnect' % disp.params['wlan'][wlan])
										Association.associate_infra(disp, disp.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
										disp.params['battery'] = disp.params['battery'] - 0.1
										# end DISPOSITIVOS QUE CONFORMAN EL GRUPO
								
							print("2_SI SE REALIZA EL CAMBIO")
							
							
							f.close()
						else:
							print("2_NO SE REALIZA EL CAMBIO - misma red")
					else:
						print("La moda es menor")
					
					del hist[3][0]
					#print(hist)
					hist[3].append(ap_n)
				else:
					print("2_ AP predicho NO esta entre los aps en rango")
					del hist[3][0]
					hist[3].append("")
					
			else:
				print("2_ NO tiene hist")
				if ap_n in aps_in_range_name:
					if str(sta.params['associatedTo'][wlan]) != str(ap_n):
						if str(sta.params['associatedTo'][wlan]) not in aps_in_range_name:
							tiempo_final = time.time()
							time_selec = tiempo_final - tiempo_inicial
							f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
							f.write("inicio del cambio el ap al que esta conectado ya no esta en rango\n")
							indice = aps_in_range_name.index(str(ap_n))
							f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
							f.write("fin del cambio\n")
							print ("CAMBIO.................................................................................")
							debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
							sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
							Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
							sta.params['battery'] = sta.params['battery'] - 0.1
							#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
							f.close()
						else:
							print("El ap al que esta concestado aun est en rango --- no se hace el cambio")
					else:
						#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
						print('misma red')
				#if ap_n in aps_temp:
				else:
					print('*******AP NOOOO ESTA EN RANGO*******')
					#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
					#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
		else:
			print('estacion no realiza seleccion de AP')
		return self.changeAP

	def rf_V5_3_SIN_Group_movility(self, sta, ap, wlan, ap_wlan):
		#rf_V5_3_SIN_Group_movility
		#rf_V5_3: Random Forest final(SIN implementacion de movilidad en grupo) con este se elimina el efecto pong pong de RF_V2_0 -- 
		print("\n---RF---")
		tiempo_inicial = time.time() 
		"""
		aps = ""
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps = aps + ap_temp2.name[2:]
		"""
		ap_names = ["ap1","ap2","ap3","ap4"]
		ind = False
		
		list_rf = []
		
		for i in range(len(ap_names)):
			for i2 in range( len(sta.params["apsInRange"]) ):
				ap_temp = sta.params['apsInRange'][i2]
				ap_temp_name = str(ap_temp.name)
				
				if ap_names[i] == ap_temp_name:
					
					# RSSI
					ap_temp_dis = sta.get_distance_to(ap_temp) # distancia del adispositivo al AP
					ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  #RSSI del dispositivo al AP
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis) #RSSI del dispositivo al AP se le resta 2
					"""
					
					
					# BATERIA
					sta_app = sta.params.get("app", 1) #Se saca que aplicacion (ninguna-1, voz-2, audio-3, video-4) corre el dispositivo
					ap_temp_con = 0.001 * ap_temp_dis * sta_app #consumo de bateria (depende de la distancia y la aplicacion del dispositivo)
					#print("ap: " + str(ap_temp.name) + " distancia: " + str(ap_temp_dis) + " app: " + str(sta_app) + " bat_temp" + str(ap_temp_con))
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_con = 0.001 * ap_temp_dis * sta_app  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_con = (0.001 * ap_temp_dis * sta_app)  #RSSI del dispositivo al AP se le resta 2
					"""
					
					# OCUPACION
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) # el numero de dispositivos se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) + 2 # al numero de dispositivos se le aumenta 2
					#ap_temp_num_sta = len(ap_temp.params['associatedStations'])
					
					ap_temp_ocu = ((ap_temp_num_sta*100.)/ap_temp.params['maxDis']) # se saca la ocupacion del AP en porcentaje
					
					# Escribir datos en dataset
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format(str(ap_temp.name), str(ap_temp_rssi), str(ap_temp_ocu),ap_temp_con))
					
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format("1", str(ap_temp_rssi), str(ap_temp_ocu), ap_temp_con))
					
					temp_list_rf = [1, ap_temp_rssi, ap_temp_ocu, ap_temp_con]
					
					list_rf.extend(temp_list_rf)
					
					ind = True
					break
				else:
					ind = False
				
			if ind == False:
				temp_list_rf = [0, -100.0, 100, 1.0]
				list_rf.extend(temp_list_rf)
				#f_datos_entrenamiento.write("{},{},{},{},".format("0", "xx", "yy","zz"))
		print("---------Array a predecir---------")
		print(list_rf)
		solution = pred([list_rf])
		ap_n = "ap{}".format(solution[0])
		
		aps_in_range_name = []
		rssi_aps_in_range = []
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps_in_range_name.append(ap_temp2.name)
			
			rssi_aptemp = sta.get_rssi(ap_temp2,0,sta.get_distance_to(ap_temp2))
			rssi_aps_in_range.append(rssi_aptemp)
			
			#aps = aps + ap_temp2.name[2:]
		
		print("aps en rango")
		print(aps_in_range_name)
		
		print("RSSI aps en rango")
		print(rssi_aps_in_range)
		
		print("aps seleccionado")
		print(ap_n)
		
		hist = sta.params.get("hist", "null")
		
		if hist != "null":
			print("2_ SI tiene hist")
			if ap_n in aps_in_range_name:
				print("2_ AP predicho SI esta entre los aps en rango")
				hist_scan = hist[3] # se saca el historial de aps_predichos
				ap_ejm = hist_scan[0] # se saca del historial un ap para comparar con los demas
				print(ap_ejm)
				mode = 1
				for i in hist_scan[1:]: #ciclo para escanear todo el historial de aps_predichos
					if ap_ejm == i: #condicion para comparar los aps 
						mode = mode+1
					else: 
						break #si no son iguales se rompe el ciclo
				print(hist_scan)
				print("mode = " + str(mode))
				
				if mode == 6: # si el historial de aps predichos son todos iguales se pasa a la siguiente etapa
					print("La moda es igual")
					if str(sta.params['associatedTo'][wlan]) != str(ap_n):
						print("2_SI SE REALIZA EL CAMBIO")
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						f.write("2_inicio del cambio el ap al que esta conectado ya no esta en rango\n")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("2_fin del cambio\n")
						print ("2_CAMBIO.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
					else:
						print("2_NO SE REALIZA EL CAMBIO - misma red")
				else:
					print("La moda es menor")
				
				del hist[3][0]
				#print(hist)
				hist[3].append(ap_n)
			else:
				print("2_ AP predicho NO esta entre los aps en rango")
				del hist[3][0]
				hist[3].append("")
				
		else:
			print("2_ NO tiene hist")
			if ap_n in aps_in_range_name:
				if str(sta.params['associatedTo'][wlan]) != str(ap_n):
					if str(sta.params['associatedTo'][wlan]) not in aps_in_range_name:
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						f.write("inicio del cambio el ap al que esta conectado ya no esta en rango\n")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("fin del cambio\n")
						print ("CAMBIO.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
					else:
						print("El ap al que esta concestado aun est en rango --- no se hace el cambio")
				else:
					#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
					print('misma red')
			#if ap_n in aps_temp:
			else:
				print('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
		
		return self.changeAP

	def rf_V5_2(self, sta, ap, wlan, ap_wlan):
		#RF: Random Forest
		
		print("\n---RF---")
		tiempo_inicial = time.time() 
		"""
		aps = ""
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps = aps + ap_temp2.name[2:]
		"""
		ap_names = ["ap1","ap2","ap3","ap4"]
		ind = False
		
		list_rf = []
		
		for i in range(len(ap_names)):
			for i2 in range( len(sta.params["apsInRange"]) ):
				ap_temp = sta.params['apsInRange'][i2]
				ap_temp_name = str(ap_temp.name)
				
				if ap_names[i] == ap_temp_name:
					
					# RSSI
					ap_temp_dis = sta.get_distance_to(ap_temp) # distancia del adispositivo al AP
					ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  #RSSI del dispositivo al AP
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis) #RSSI del dispositivo al AP se le resta 2
					"""
					
					
					# BATERIA
					sta_app = sta.params.get("app", 1) #Se saca que aplicacion (ninguna-1, voz-2, audio-3, video-4) corre el dispositivo
					ap_temp_con = 0.001 * ap_temp_dis * sta_app #consumo de bateria (depende de la distancia y la aplicacion del dispositivo)
					#print("ap: " + str(ap_temp.name) + " distancia: " + str(ap_temp_dis) + " app: " + str(sta_app) + " bat_temp" + str(ap_temp_con))
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_con = 0.001 * ap_temp_dis * sta_app  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_con = (0.001 * ap_temp_dis * sta_app)  #RSSI del dispositivo al AP se le resta 2
					"""
					
					# OCUPACION
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) # el numero de dispositivos se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) + 2 # al numero de dispositivos se le aumenta 2
					#ap_temp_num_sta = len(ap_temp.params['associatedStations'])
					
					ap_temp_ocu = ((ap_temp_num_sta*100.)/ap_temp.params['maxDis']) # se saca la ocupacion del AP en porcentaje
					
					# Escribir datos en dataset
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format(str(ap_temp.name), str(ap_temp_rssi), str(ap_temp_ocu),ap_temp_con))
					
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format("1", str(ap_temp_rssi), str(ap_temp_ocu), ap_temp_con))
					
					temp_list_rf = [1, ap_temp_rssi, ap_temp_ocu, ap_temp_con]
					
					list_rf.extend(temp_list_rf)
					
					ind = True
					break
				else:
					ind = False
				
			if ind == False:
				temp_list_rf = [0, -100.0, 100, 1.0]
				list_rf.extend(temp_list_rf)
				#f_datos_entrenamiento.write("{},{},{},{},".format("0", "xx", "yy","zz"))
		print("---------Array a predecir---------")
		print(list_rf)
		solution = pred([list_rf])
		ap_n = "ap{}".format(solution[0])
		
		aps_in_range_name = []
		rssi_aps_in_range = []
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps_in_range_name.append(ap_temp2.name)
			
			rssi_aptemp = sta.get_rssi(ap_temp2,0,sta.get_distance_to(ap_temp2))
			rssi_aps_in_range.append(rssi_aptemp)
			
			#aps = aps + ap_temp2.name[2:]
		
		print("aps en rango")
		print(aps_in_range_name)
		
		print("RSSI aps en rango")
		print(rssi_aps_in_range)
		
		print("aps seleccionado")
		print(ap_n)
		
		hist = sta.params.get("hist", "null")
		
		if hist != "null":
			print("2_con hist")
			#var = self.params.get("associatedTo", "null")[0]
			#print var
			#print(str(type(var)))
			if ap_n not in aps_in_range_name:
				#if type(var) == str:
				del hist[3][0]
				#print(hist)
				hist[3].append("")
				print("2_ap predicho no esta en rango")
				#print(hist)
				#print("es " + str(type(var)))
			else:
				hist_scan = hist[3]
				ap_ejm = hist_scan[0]
				print(ap_ejm)
				mode = 1
				for i in hist_scan[1:]:
					if ap_ejm == i:
						mode = mode+1
					else: 
						break
				print(hist_scan)
				print("mode = " + str(mode))
				
				
				if mode == 14:
					if str(sta.params['associatedTo'][wlan]) != str(ap_n):
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						f.write("2_inicio del cambio el ap al que esta conectado ya no esta en rango\n")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("2_fin del cambio\n")
						print ("2_CAMBIO.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
					else:
						print('2_misma red')
				elif str(sta.params['associatedTo'][wlan]) not in aps_in_range_name:
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						f.write("2_1_inicio del cambio el ap al que esta conectado ya no esta en rango\n")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("2_1_fin del cambio\n")
						print ("2_1_CAMBIO_ el ap al que estaba conectado noesta en rango.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
				else:
					print("2_NO se hace el cambio, la moda es distinta de 3")
					print("El ap aun esta en rango")
					
				del hist[3][0]
				#print(hist)
				hist[3].append(ap_n)
				#print(hist)
				#print("NO, es " + str(type(var)))
		else:
			print("sin hist")
			if ap_n in aps_in_range_name:
				if str(sta.params['associatedTo'][wlan]) != str(ap_n):
					if str(sta.params['associatedTo'][wlan]) not in aps_in_range_name:
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						f.write("inicio del cambio el ap al que esta conectado ya no esta en rango\n")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("fin del cambio\n")
						print ("CAMBIO.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
					else:
						print("El ap al que esta concestado aun est en rango --- no se hace el cambio")
				else:
					#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
					print('misma red')
			#if ap_n in aps_temp:
			else:
				print('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
			
		return self.changeAP



	def rf_V5_1(self, sta, ap, wlan, ap_wlan):
		#RF: Random Forest
		print("\n---RF---")
		tiempo_inicial = time.time() 
		"""
		aps = ""
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps = aps + ap_temp2.name[2:]
		"""
		ap_names = ["ap1","ap2","ap3","ap4"]
		ind = False
		
		list_rf = []
		
		for i in range(len(ap_names)):
			for i2 in range( len(sta.params["apsInRange"]) ):
				ap_temp = sta.params['apsInRange'][i2]
				ap_temp_name = str(ap_temp.name)
				
				if ap_names[i] == ap_temp_name:
					
					# RSSI
					ap_temp_dis = sta.get_distance_to(ap_temp) # distancia del adispositivo al AP
					ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  #RSSI del dispositivo al AP
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis) #RSSI del dispositivo al AP se le resta 2
					"""
					
					
					# BATERIA
					sta_app = sta.params.get("app", 1) #Se saca que aplicacion (ninguna-1, voz-2, audio-3, video-4) corre el dispositivo
					ap_temp_con = 0.001 * ap_temp_dis * sta_app #consumo de bateria (depende de la distancia y la aplicacion del dispositivo)
					#print("ap: " + str(ap_temp.name) + " distancia: " + str(ap_temp_dis) + " app: " + str(sta_app) + " bat_temp" + str(ap_temp_con))
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_con = 0.001 * ap_temp_dis * sta_app  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_con = (0.001 * ap_temp_dis * sta_app)  #RSSI del dispositivo al AP se le resta 2
					"""
					
					# OCUPACION
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) # el numero de dispositivos se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) + 2 # al numero de dispositivos se le aumenta 2
					#ap_temp_num_sta = len(ap_temp.params['associatedStations'])
					
					ap_temp_ocu = ((ap_temp_num_sta*100.)/ap_temp.params['maxDis']) # se saca la ocupacion del AP en porcentaje
					
					# Escribir datos en dataset
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format(str(ap_temp.name), str(ap_temp_rssi), str(ap_temp_ocu),ap_temp_con))
					
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format("1", str(ap_temp_rssi), str(ap_temp_ocu), ap_temp_con))
					
					temp_list_rf = [1, ap_temp_rssi, ap_temp_ocu, ap_temp_con]
					
					list_rf.extend(temp_list_rf)
					
					ind = True
					break
				else:
					ind = False
				
			if ind == False:
				temp_list_rf = [0, -100.0, 100, 1.0]
				list_rf.extend(temp_list_rf)
				#f_datos_entrenamiento.write("{},{},{},{},".format("0", "xx", "yy","zz"))
		print("---------Array a predecir---------")
		print(list_rf)
		solution = pred([list_rf])
		ap_n = "ap{}".format(solution[0])
		
		aps_in_range_name = []
		rssi_aps_in_range = []
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps_in_range_name.append(ap_temp2.name)
			
			rssi_aptemp = sta.get_rssi(ap_temp2,0,sta.get_distance_to(ap_temp2))
			rssi_aps_in_range.append(rssi_aptemp)
			
			#aps = aps + ap_temp2.name[2:]
		
		print("aps en rango")
		print(aps_in_range_name)
		
		print("RSSI aps en rango")
		print(rssi_aps_in_range)
		
		print("aps seleccionado")
		print(ap_n)
		
		hist = sta.params.get("hist", "null")
		
		if hist != "null":
			print("2_con hist")
			#var = self.params.get("associatedTo", "null")[0]
			#print var
			#print(str(type(var)))
			if ap_n not in aps_in_range_name:
				#if type(var) == str:
				del hist[3][0]
				#print(hist)
				hist[3].append("")
				print("2_ap predicho no esta en rango")
				#print(hist)
				#print("es " + str(type(var)))
			else:
				hist_scan = hist[3]
				ap_ejm = hist_scan[0]
				print(ap_ejm)
				mode = 1
				for i in hist_scan[1:]:
					if ap_ejm == i:
						mode = mode+1
					else: 
						break
				print(hist_scan)
				print("mode = " + str(mode))
				
				
				if mode == 11:
					if str(sta.params['associatedTo'][wlan]) != str(ap_n):
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						f.write("2_inicio del cambio el ap al que esta conectado ya no esta en rango\n")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("2_fin del cambio\n")
						print ("2_CAMBIO.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
					else:
						print('2_misma red')
				elif str(sta.params['associatedTo'][wlan]) not in aps_in_range_name:
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						f.write("2_1_inicio del cambio el ap al que esta conectado ya no esta en rango\n")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("2_1_fin del cambio\n")
						print ("2_1_CAMBIO_ el ap al que estaba conectado noesta en rango.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
				else:
					print("2_NO se hace el cambio, la moda es distinta de 3")
					print("El ap aun esta en rango")
					
				del hist[3][0]
				#print(hist)
				hist[3].append(ap_n)
				#print(hist)
				#print("NO, es " + str(type(var)))
		else:
			print("sin hist")
			if ap_n in aps_in_range_name:
				if str(sta.params['associatedTo'][wlan]) != str(ap_n):
					if str(sta.params['associatedTo'][wlan]) not in aps_in_range_name:
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						f.write("inicio del cambio el ap al que esta conectado ya no esta en rango\n")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("fin del cambio\n")
						print ("CAMBIO.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
					else:
						print("El ap al que esta concestado aun est en rango --- no se hace el cambio")
				else:
					#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
					print('misma red')
			#if ap_n in aps_temp:
			else:
				print('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
			
		return self.changeAP


	def rf_V5_0(self, sta, ap, wlan, ap_wlan):
		#RF: Random Forest
		print("\n---RF---")
		tiempo_inicial = time.time() 
		"""
		aps = ""
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps = aps + ap_temp2.name[2:]
		"""
		ap_names = ["ap1","ap2","ap3","ap4"]
		ind = False
		
		list_rf = []
		
		for i in range(len(ap_names)):
			for i2 in range( len(sta.params["apsInRange"]) ):
				ap_temp = sta.params['apsInRange'][i2]
				ap_temp_name = str(ap_temp.name)
				
				if ap_names[i] == ap_temp_name:
					
					# RSSI
					ap_temp_dis = sta.get_distance_to(ap_temp) # distancia del adispositivo al AP
					ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  #RSSI del dispositivo al AP
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis) #RSSI del dispositivo al AP se le resta 2
					"""
					
					
					# BATERIA
					sta_app = sta.params.get("app", 1) #Se saca que aplicacion (ninguna-1, voz-2, audio-3, video-4) corre el dispositivo
					ap_temp_con = 0.001 * ap_temp_dis * sta_app #consumo de bateria (depende de la distancia y la aplicacion del dispositivo)
					#print("ap: " + str(ap_temp.name) + " distancia: " + str(ap_temp_dis) + " app: " + str(sta_app) + " bat_temp" + str(ap_temp_con))
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_con = 0.001 * ap_temp_dis * sta_app  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_con = (0.001 * ap_temp_dis * sta_app)  #RSSI del dispositivo al AP se le resta 2
					"""
					
					# OCUPACION
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) # el numero de dispositivos se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) + 2 # al numero de dispositivos se le aumenta 2
					#ap_temp_num_sta = len(ap_temp.params['associatedStations'])
					
					ap_temp_ocu = ((ap_temp_num_sta*100.)/ap_temp.params['maxDis']) # se saca la ocupacion del AP en porcentaje
					
					# Escribir datos en dataset
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format(str(ap_temp.name), str(ap_temp_rssi), str(ap_temp_ocu),ap_temp_con))
					
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format("1", str(ap_temp_rssi), str(ap_temp_ocu), ap_temp_con))
					
					temp_list_rf = [1, ap_temp_rssi, ap_temp_ocu, ap_temp_con]
					
					list_rf.extend(temp_list_rf)
					
					ind = True
					break
				else:
					ind = False
				
			if ind == False:
				temp_list_rf = [0, -100.0, 100, 1.0]
				list_rf.extend(temp_list_rf)
				#f_datos_entrenamiento.write("{},{},{},{},".format("0", "xx", "yy","zz"))
		print("---------Array a predecir---------")
		print(list_rf)
		solution = pred([list_rf])
		ap_n = "ap{}".format(solution[0])
		
		aps_in_range_name = []
		rssi_aps_in_range = []
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps_in_range_name.append(ap_temp2.name)
			
			rssi_aptemp = sta.get_rssi(ap_temp2,0,sta.get_distance_to(ap_temp2))
			rssi_aps_in_range.append(rssi_aptemp)
			
			#aps = aps + ap_temp2.name[2:]
		
		print("aps en rango")
		print(aps_in_range_name)
		
		print("RSSI aps en rango")
		print(rssi_aps_in_range)
		
		print("aps seleccionado")
		print(ap_n)
		
		"""
		#indice = aps_in_range_rssi.index(max(aps_in_range_rssi))
		rssi_max = max(rssi_aps_in_range)
		n=0
		
		ap_candidates_rssi = []
		
		for rssi_ap in rssi_aps_in_range:
			if rssi_max == rssi_ap:
				#print n
				print(rssi_aps_in_range[n])
				print(aps_in_range_name[n])
				ap_candidates_rssi.append(aps_in_range_name[n])
				#print (i)
			n = n+1
		print(ap_candidates_rssi)
		"""
		hist = sta.params.get("hist", "null")
		
		if hist != "null":
			print("2_con hist")
			#var = self.params.get("associatedTo", "null")[0]
			#print var
			#print(str(type(var)))
			if ap_n not in aps_in_range_name:
				#if type(var) == str:
				del hist[3][0]
				#print(hist)
				hist[3].append("")
				print("2_ap predicho no esta en rango")
				#print(hist)
				#print("es " + str(type(var)))
			else:
				hist_scan = hist[3]
				ap_ejm = hist_scan[0]
				print(ap_ejm)
				mode = 1
				for i in hist_scan[1:]:
					if ap_ejm == i:
						mode = mode+1
					else: 
						break
				print(hist_scan)
				print("mode = " + str(mode))
				
				
				if mode == 3:
					if str(sta.params['associatedTo'][wlan]) != str(ap_n):
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						f.write("2_inicio del cambio el ap al que esta conectado ya no esta en rango\n")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("2_fin del cambio\n")
						print ("2_CAMBIO.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
					else:
						print('2_misma red')
				elif str(sta.params['associatedTo'][wlan]) not in aps_in_range_name:
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						f.write("2_inicio del cambio el ap al que esta conectado ya no esta en rango\n")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("2_fin del cambio\n")
						print ("2_CAMBIO_ el ap al que estaba conectado noesta en rango.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
				else:
					print("2_NO se hace el cambio, la moda es distinta de 3")
					print("El ap aun esta en rango")
					
				del hist[3][0]
				#print(hist)
				hist[3].append(ap_n)
				#print(hist)
				#print("NO, es " + str(type(var)))
		else:
			print("sin hist")
			if ap_n in aps_in_range_name:
				if str(sta.params['associatedTo'][wlan]) != str(ap_n):
					if str(sta.params['associatedTo'][wlan]) not in aps_in_range_name:
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						f.write("inicio del cambio el ap al que esta conectado ya no esta en rango\n")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("fin del cambio\n")
						print ("CAMBIO.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
					else:
						print("El ap al que esta concestado aun est en rango --- no se hace el cambio")
				else:
					#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
					print('misma red')
			#if ap_n in aps_temp:
			else:
				print('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
			
		"""
		if ap_n in aps_in_range_name:
			#f_2.write("****{},{}\n".format(aps_temp,ap_n))
			if str(sta.params['associatedTo'][wlan]) != str(ap_n):
				tiempo_final = time.time()
				time_selec = tiempo_final - tiempo_inicial
				
				#f_2.write("**************************************SI Cambio de AP{}-------------------------\n".format(mode[0][0]))
				#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
				#f_2.write("ap_n: {}, array_indice: {}, array_ap: {}, ap: {}\n".format(ap_n, indice, aps_temp[indice], sta.params['apsInRange'][indice]))
				#f_2.write("-------------------------\n")
				
				#print("El AP - {} esta en la posicion {} de la lista".format(ap_n,indice))
				indice = aps_in_range_name.index(str(ap_n))
				f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
				#f.write("{},{},{}\n".format(sta.name, str(sta.params['associatedTo'][wlan]),mrf))
				f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
				#f.write('{"time":"%s", "sta":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s", "oldAp":"%s", "newAp":"%s"}\n' %(str(time_selec*1000),str(sta.name), str(aps_temp), str(sta.params['battery']), str(sta.params['position']), str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()])))
				debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
				sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
				Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
				sta.params['battery'] = sta.params['battery'] - 0.1
				#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
				f.close()
			else:
				#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
				print('misma red')
		#if ap_n in aps_temp:
		else:
			print('*******AP NOOOO ESTA EN RANGO*******')
			#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
			#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
		"""
		return self.changeAP
		

	def rf_v4(self, sta, ap, wlan, ap_wlan):
		#RF: Random Forest
		print("\n---RF---")
		tiempo_inicial = time.time() 
		"""
		aps = ""
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps = aps + ap_temp2.name[2:]
		"""
		ap_names = ["ap1","ap2","ap3","ap4"]
		ind = False
		
		list_rf = []
		
		for i in range(len(ap_names)):
			for i2 in range( len(sta.params["apsInRange"]) ):
				ap_temp = sta.params['apsInRange'][i2]
				ap_temp_name = str(ap_temp.name)
				
				if ap_names[i] == ap_temp_name:
					
					# RSSI
					ap_temp_dis = sta.get_distance_to(ap_temp) # distancia del adispositivo al AP
					ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  #RSSI del dispositivo al AP
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis) #RSSI del dispositivo al AP se le resta 2
					"""
					
					
					# BATERIA
					sta_app = sta.params.get("app", 1) #Se saca que aplicacion (ninguna-1, voz-2, audio-3, video-4) corre el dispositivo
					ap_temp_con = 0.001 * ap_temp_dis * sta_app #consumo de bateria (depende de la distancia y la aplicacion del dispositivo)
					#print("ap: " + str(ap_temp.name) + " distancia: " + str(ap_temp_dis) + " app: " + str(sta_app) + " bat_temp" + str(ap_temp_con))
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_con = 0.001 * ap_temp_dis * sta_app  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_con = (0.001 * ap_temp_dis * sta_app)  #RSSI del dispositivo al AP se le resta 2
					"""
					
					# OCUPACION
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) # el numero de dispositivos se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) + 2 # al numero de dispositivos se le aumenta 2
					#ap_temp_num_sta = len(ap_temp.params['associatedStations'])
					
					ap_temp_ocu = ((ap_temp_num_sta*100.)/ap_temp.params['maxDis']) # se saca la ocupacion del AP en porcentaje
					
					# Escribir datos en dataset
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format(str(ap_temp.name), str(ap_temp_rssi), str(ap_temp_ocu),ap_temp_con))
					
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format("1", str(ap_temp_rssi), str(ap_temp_ocu), ap_temp_con))
					
					temp_list_rf = [1, ap_temp_rssi, ap_temp_ocu, ap_temp_con]
					
					list_rf.extend(temp_list_rf)
					
					ind = True
					break
				else:
					ind = False
				
			if ind == False:
				temp_list_rf = [0, -100.0, 100, 1.0]
				list_rf.extend(temp_list_rf)
				#f_datos_entrenamiento.write("{},{},{},{},".format("0", "xx", "yy","zz"))
		print("---------Array a predecir---------")
		print(list_rf)
		solution = pred([list_rf])
		ap_n = "ap{}".format(solution[0])
		
		aps_in_range_name = []
		rssi_aps_in_range = []
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps_in_range_name.append(ap_temp2.name)
			
			rssi_aptemp = sta.get_rssi(ap_temp2,0,sta.get_distance_to(ap_temp2))
			rssi_aps_in_range.append(rssi_aptemp)
			
			#aps = aps + ap_temp2.name[2:]
		
		print("aps en rango")
		print(aps_in_range_name)
		
		print("RSSI aps en rango")
		print(rssi_aps_in_range)
		
		print("aps seleccionado")
		print(ap_n)
		
		
		#indice = aps_in_range_rssi.index(max(aps_in_range_rssi))
		rssi_max = max(rssi_aps_in_range)
		n=0
		
		ap_candidates_rssi = []
		
		for rssi_ap in rssi_aps_in_range:
			if rssi_max == rssi_ap:
				#print n
				print(rssi_aps_in_range[n])
				print(aps_in_range_name[n])
				ap_candidates_rssi.append(aps_in_range_name[n])
				#print (i)
			n = n+1
		print(ap_candidates_rssi)
		
		if ap_n in aps_in_range_name:
			if str(sta.params['associatedTo'][wlan]) != str(ap_n):
				if str(sta.params['associatedTo'][wlan]) not in aps_in_range_name:
					tiempo_final = time.time()
					time_selec = tiempo_final - tiempo_inicial
					f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
					f.write("inicio del cambio el ap al que esta conectado ya no esta en rango\n")
					indice = aps_in_range_name.index(str(ap_n))
					f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
					f.write("fin del cambio\n")
					print ("CAMBIO.................................................................................")
					print ("CAMBIO.................................................................................")
					debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
					sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
					Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
					sta.params['battery'] = sta.params['battery'] - 0.1
					#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
					f.close()
				else:
					if ap_n in ap_candidates_rssi:
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						f.write("inicio del cambio el ap al qu esta conectado aun esta en rango")
						indice = aps_in_range_name.index(str(ap_n))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						f.write("fin del cambio")
						print ("CAMBIO.................................................................................")
						print ("CAMBIO.................................................................................")
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
					else:
						print('No esta entre los ap candidatos')
			else:
				#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
				print('misma red')
		#if ap_n in aps_temp:
		else:
			print('*******AP NOOOO ESTA EN RANGO*******')
			#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
			#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
		
		"""
		if ap_n in aps_in_range_name:
			#f_2.write("****{},{}\n".format(aps_temp,ap_n))
			if str(sta.params['associatedTo'][wlan]) != str(ap_n):
				tiempo_final = time.time()
				time_selec = tiempo_final - tiempo_inicial
				
				#f_2.write("**************************************SI Cambio de AP{}-------------------------\n".format(mode[0][0]))
				#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
				#f_2.write("ap_n: {}, array_indice: {}, array_ap: {}, ap: {}\n".format(ap_n, indice, aps_temp[indice], sta.params['apsInRange'][indice]))
				#f_2.write("-------------------------\n")
				
				#print("El AP - {} esta en la posicion {} de la lista".format(ap_n,indice))
				indice = aps_in_range_name.index(str(ap_n))
				f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
				#f.write("{},{},{}\n".format(sta.name, str(sta.params['associatedTo'][wlan]),mrf))
				f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
				#f.write('{"time":"%s", "sta":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s", "oldAp":"%s", "newAp":"%s"}\n' %(str(time_selec*1000),str(sta.name), str(aps_temp), str(sta.params['battery']), str(sta.params['position']), str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()])))
				debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
				sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
				Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
				sta.params['battery'] = sta.params['battery'] - 0.1
				#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
				f.close()
			else:
				#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
				print('misma red')
		#if ap_n in aps_temp:
		else:
			print('*******AP NOOOO ESTA EN RANGO*******')
			#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
			#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
		"""
		return self.changeAP
		

	def rf_v3(self, sta, ap, wlan, ap_wlan):
		#RF: Random Forest
		print("\n---RF---")
		tiempo_inicial = time.time() 
		"""
		aps = ""
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps = aps + ap_temp2.name[2:]
		"""
		ap_names = ["ap1","ap2","ap3","ap4"]
		ind = False
		
		list_rf = []
		
		for i in range(len(ap_names)):
			for i2 in range( len(sta.params["apsInRange"]) ):
				ap_temp = sta.params['apsInRange'][i2]
				ap_temp_name = str(ap_temp.name)
				
				if ap_names[i] == ap_temp_name:
					
					# RSSI
					ap_temp_dis = sta.get_distance_to(ap_temp) # distancia del adispositivo al AP
					ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  #RSSI del dispositivo al AP
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis) #RSSI del dispositivo al AP se le resta 2
					"""
					
					
					# BATERIA
					sta_app = sta.params.get("app", 1) #Se saca que aplicacion (ninguna-1, voz-2, audio-3, video-4) corre el dispositivo
					ap_temp_con = 0.001 * ap_temp_dis * sta_app #consumo de bateria (depende de la distancia y la aplicacion del dispositivo)
					#print("ap: " + str(ap_temp.name) + " distancia: " + str(ap_temp_dis) + " app: " + str(sta_app) + " bat_temp" + str(ap_temp_con))
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_con = 0.001 * ap_temp_dis * sta_app  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_con = (0.001 * ap_temp_dis * sta_app)  #RSSI del dispositivo al AP se le resta 2
					"""
					
					# OCUPACION
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) # el numero de dispositivos se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) + 2 # al numero de dispositivos se le aumenta 2
					#ap_temp_num_sta = len(ap_temp.params['associatedStations'])
					
					ap_temp_ocu = ((ap_temp_num_sta*100.)/ap_temp.params['maxDis']) # se saca la ocupacion del AP en porcentaje
					
					# Escribir datos en dataset
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format(str(ap_temp.name), str(ap_temp_rssi), str(ap_temp_ocu),ap_temp_con))
					
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format("1", str(ap_temp_rssi), str(ap_temp_ocu), ap_temp_con))
					
					temp_list_rf = [1, ap_temp_rssi, ap_temp_ocu, ap_temp_con]
					
					list_rf.extend(temp_list_rf)
					
					ind = True
					break
				else:
					ind = False
				
			if ind == False:
				temp_list_rf = [0, -100.0, 100, 1.0]
				list_rf.extend(temp_list_rf)
				#f_datos_entrenamiento.write("{},{},{},{},".format("0", "xx", "yy","zz"))
		print("---------Array a predecir---------")
		print(list_rf)
		solution = pred([list_rf])
		ap_n = "ap{}".format(solution[0])
		
		aps_in_range_name = []
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps_in_range_name.append(ap_temp2.name)
			#aps = aps + ap_temp2.name[2:]
		
		print("aps en rango")
		print(aps_in_range_name)
		
		print("aps seleccionado")
		print(ap_n)
		
		hist = sta.params.get("hist", "null")
		print (hist)
		print(ap_n)
		
		if hist != "null":
			if ap_n not in hist[2]:# si el ap_nuevo no esta en el historial de los ultimos 3 movimientos
				print("SI se hace cambio")
				print (hist[2])
				print(ap_n)
				
				if ap_n in aps_in_range_name:
					#f_2.write("****{},{}\n".format(aps_temp,ap_n))
					if str(sta.params['associatedTo'][wlan]) != str(ap_n):
						tiempo_final = time.time()
						time_selec = tiempo_final - tiempo_inicial
						"""
						f_2.write("**************************************SI Cambio de AP{}-------------------------\n".format(mode[0][0]))
						f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
						f_2.write("ap_n: {}, array_indice: {}, array_ap: {}, ap: {}\n".format(ap_n, indice, aps_temp[indice], sta.params['apsInRange'][indice]))
						f_2.write("-------------------------\n")
						"""
						#print("El AP - {} esta en la posicion {} de la lista".format(ap_n,indice))
						indice = aps_in_range_name.index(str(ap_n))
						f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
						#f.write("{},{},{}\n".format(sta.name, str(sta.params['associatedTo'][wlan]),mrf))
						f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
						#f.write('{"time":"%s", "sta":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s", "oldAp":"%s", "newAp":"%s"}\n' %(str(time_selec*1000),str(sta.name), str(aps_temp), str(sta.params['battery']), str(sta.params['position']), str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()])))
						debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
						sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
						Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
						sta.params['battery'] = sta.params['battery'] - 0.1
						#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
						f.close()
					else:
						#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
						print('misma red')
				#if ap_n in aps_temp:
				else:
					print('*******AP NOOOO ESTA EN RANGO*******')
					#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
					#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
			else:
				print("NO se hace cambio")
		else:
			print("No tiene historial")
			if ap_n in aps_in_range_name:
				#f_2.write("****{},{}\n".format(aps_temp,ap_n))
				if str(sta.params['associatedTo'][wlan]) != str(ap_n):
					tiempo_final = time.time()
					time_selec = tiempo_final - tiempo_inicial
					"""
					f_2.write("**************************************SI Cambio de AP{}-------------------------\n".format(mode[0][0]))
					f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
					f_2.write("ap_n: {}, array_indice: {}, array_ap: {}, ap: {}\n".format(ap_n, indice, aps_temp[indice], sta.params['apsInRange'][indice]))
					f_2.write("-------------------------\n")
					"""
					#print("El AP - {} esta en la posicion {} de la lista".format(ap_n,indice))
					indice = aps_in_range_name.index(str(ap_n))
					f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
					#f.write("{},{},{}\n".format(sta.name, str(sta.params['associatedTo'][wlan]),mrf))
					f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
					#f.write('{"time":"%s", "sta":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s", "oldAp":"%s", "newAp":"%s"}\n' %(str(time_selec*1000),str(sta.name), str(aps_temp), str(sta.params['battery']), str(sta.params['position']), str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()])))
					debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
					sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
					Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
					sta.params['battery'] = sta.params['battery'] - 0.1
					#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
					f.close()
				else:
					#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
					print('misma red')
			#if ap_n in aps_temp:
			else:
				print('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
		return self.changeAP

	def rf_V2_0(self, sta, ap, wlan, ap_wlan):
		#rf_V2_0: Random Forest inicial_ con este se producen los efectos ping_pong
		print("\n---RF---")
		tiempo_inicial = time.time() 
		"""
		aps = ""
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps = aps + ap_temp2.name[2:]
		"""
		ap_names = ["ap1","ap2","ap3","ap4"]
		ind = False
		
		list_rf = []
		
		for i in range(len(ap_names)):
			for i2 in range( len(sta.params["apsInRange"]) ):
				ap_temp = sta.params['apsInRange'][i2]
				ap_temp_name = str(ap_temp.name)
				
				if ap_names[i] == ap_temp_name:
					
					# RSSI
					ap_temp_dis = sta.get_distance_to(ap_temp) # distancia del adispositivo al AP
					ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  #RSSI del dispositivo al AP
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis)  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_rssi = sta.get_rssi(ap_temp,0,ap_temp_dis) #RSSI del dispositivo al AP se le resta 2
					"""
					
					
					# BATERIA
					sta_app = sta.params.get("app", 1) #Se saca que aplicacion (ninguna-1, voz-2, audio-3, video-4) corre el dispositivo
					ap_temp_con = 0.001 * ap_temp_dis * sta_app #consumo de bateria (depende de la distancia y la aplicacion del dispositivo)
					#print("ap: " + str(ap_temp.name) + " distancia: " + str(ap_temp_dis) + " app: " + str(sta_app) + " bat_temp" + str(ap_temp_con))
					"""
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_con = 0.001 * ap_temp_dis * sta_app  # RSSI del dispositivo al AP se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_con = (0.001 * ap_temp_dis * sta_app)  #RSSI del dispositivo al AP se le resta 2
					"""
					
					# OCUPACION
					if ap_temp_name == str(sta.params['associatedTo'][wlan]): # si el AP que esta escaneando es igual al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) # el numero de dispositivos se mantiene
					else: #si el AP que esta escaneando es DIFERENTE al Ap al que esta conectado:
						ap_temp_num_sta = len(ap_temp.params['associatedStations']) + 2 # al numero de dispositivos se le aumenta 2
					#ap_temp_num_sta = len(ap_temp.params['associatedStations'])
					
					ap_temp_ocu = ((ap_temp_num_sta*100.)/ap_temp.params['maxDis']) # se saca la ocupacion del AP en porcentaje
					
					# Escribir datos en dataset
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format(str(ap_temp.name), str(ap_temp_rssi), str(ap_temp_ocu),ap_temp_con))
					
					#f_datos_entrenamiento.write("{},{},{},{:.4f},".format("1", str(ap_temp_rssi), str(ap_temp_ocu), ap_temp_con))
					
					temp_list_rf = [1, ap_temp_rssi, ap_temp_ocu, ap_temp_con]
					
					list_rf.extend(temp_list_rf)
					
					ind = True
					break
				else:
					ind = False
				
			if ind == False:
				temp_list_rf = [0, -100.0, 100, 1.0]
				list_rf.extend(temp_list_rf)
				#f_datos_entrenamiento.write("{},{},{},{},".format("0", "xx", "yy","zz"))
		print("---------Array a predecir---------")
		print(list_rf)
		solution = pred([list_rf])
		ap_n = "ap{}".format(solution[0])
		
		aps_in_range_name = []
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps_in_range_name.append(ap_temp2.name)
			#aps = aps + ap_temp2.name[2:]
		
		print("aps en rango")
		print(aps_in_range_name)
		
		print("aps seleccionado")
		print(ap_n)
		
		if ap_n in aps_in_range_name:
			#f_2.write("****{},{}\n".format(aps_temp,ap_n))
			if str(sta.params['associatedTo'][wlan]) != str(ap_n):
				tiempo_final = time.time()
				time_selec = tiempo_final - tiempo_inicial
				"""
				f_2.write("**************************************SI Cambio de AP{}-------------------------\n".format(mode[0][0]))
				f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
				f_2.write("ap_n: {}, array_indice: {}, array_ap: {}, ap: {}\n".format(ap_n, indice, aps_temp[indice], sta.params['apsInRange'][indice]))
				f_2.write("-------------------------\n")
				"""
				#print("El AP - {} esta en la posicion {} de la lista".format(ap_n,indice))
				indice = aps_in_range_name.index(str(ap_n))
				f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
				#f.write("{},{},{}\n".format(sta.name, str(sta.params['associatedTo'][wlan]),mrf))
				f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_in_range_name), str(sta.params['battery']), str(sta.params['position'])))
				#f.write('{"time":"%s", "sta":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s", "oldAp":"%s", "newAp":"%s"}\n' %(str(time_selec*1000),str(sta.name), str(aps_temp), str(sta.params['battery']), str(sta.params['position']), str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()])))
				debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
				sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
				Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
				sta.params['battery'] = sta.params['battery'] - 0.1
				#sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
				f.close()
			else:
				#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
				print('misma red')
		#if ap_n in aps_temp:
		else:
			print('*******AP NOOOO ESTA EN RANGO*******')
			#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
			#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
		
		return self.changeAP

	def rf_v1(self, sta, ap, wlan, ap_wlan):
		#RF: Random Forest
		print("\n---RF---")
		tiempo_inicial = time.time() 
		md = np.array([])						#MATRIZ DE DECISION
		#mp = np.array([ 2./6, 1./6, 3./6])		#VECTOR DE PESOS
		#mp = np.array([ 2./5., 2./5., 1./5.])
		#mp = np.array([ 0.4, 0.6])
		#mp = np.array([ 0.3, 0.5, 0.2])
		Alist = [r for r in md]
		aps_temp = []
		
		mrf = np.array([])
		Alistrf = [r for r in mrf]
		
		aps = ""
		for n in range( len(sta.params["apsInRange"]) ):
			ap_temp2 = sta.params['apsInRange'][n]
			aps = aps + ap_temp2.name[2:]
		
		for i in range( len(sta.params["apsInRange"]) ):
			ap_temp = sta.params['apsInRange'][i]
			rssi_aptemp = sta.get_rssi(ap_temp,0,sta.get_distance_to(ap_temp))
			#n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta.get_distance_to(ap_temp)
			if str(ap_temp.name) == str(sta.params['associatedTo'][wlan]):
				n_est_aptemp = len(ap_temp.params['associatedStations'])
			else:
				n_est_aptemp = len(ap_temp.params['associatedStations']) + 2
			
			dis_to_aptemp = sta.get_distance_to(ap_temp)
			
			bat_temp = 0.01 * dis_to_aptemp
			
			n2_est_aptemp = len(ap_temp.params['associatedStations'])
			
			
			"""
			f_1= open("/home/mininet/Escritorio/scripts/output/datosML4.txt","a+")
			f_1.write("{},{},{},{},{},{},{},{}\n".format(str(sta.name), str(aps), str(ap_temp.name[2:]), str(rssi_aptemp), str(n2_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta.params['associatedTo'][wlan])))
			f_1.close()
			"""
			"""
			print ("AP name %s" %ap_temp.name )
			print ("RSSI %s" %str(rssi_aptemp) )
			print ("# estations %s" %str(n_est_aptemp) )
			print ("Distance to AP %s" %str(dis_to_aptemp) )
			"""
			
			#newrow = [ap_temp.name, rssi_aptemp, n_est_aptemp, dis_to_aptemp]
			#newrow = [rssi_aptemp, n_est_aptemp*-1, dis_to_aptemp*1000]
			#newrow = [rssi_aptemp*-1, n_est_aptemp, dis_to_aptemp]
			newrow = [rssi_aptemp*-1, n_est_aptemp, bat_temp]
			Alist.append(newrow)
			aps_temp.append(ap_temp.name)
			
			newrowrf = [aps,ap_temp.name[2:],rssi_aptemp, n2_est_aptemp, bat_temp]
			Alistrf.append(newrowrf)
			
			
			#n2_est_aptemp = len(ap_temp.params['associatedStations'])
			#f= open("/home/mininet/Escritorio/scripts/output/datosML3.txt","a+")
			#f.write("{},{},{},{},{},{},{}\n".format(str(sta.name), str(ap_temp.name), str(rssi_aptemp), str(n2_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta.params['associatedTo'][wlan])))
			#f.close()
		
		
		
		md = np.array(Alist)
		
		mrf = np.array(Alistrf)
		#tiempo_inicial = time.time() 
		sol = pred(mrf)
		#tiempo_final = time.time()
		#time_selec = tiempo_final - tiempo_inicial
		
		
		mode= stats.mode(sol)
		"""
		f_2= open("/home/mininet/Escritorio/scripts/output/datosML5.txt","a+")
		f_2.write("*********************************\n")
		f_2.write("{},{},{}\n".format(sta.name, str(sta.params['associatedTo'][wlan]),mrf))
		f_2.write("{},{}\n".format(sol,mode))
		f_2.write("ap{}\n".format(mode[0][0]))
		"""
		ap_n = "ap{}".format(mode[0][0])
		
		if mode[1][0] > 1:
			#f_2.write("-------------------------Cambio de AP{}-------------------------\n".format(mode[0][0]))
			#f_2.write("ap{}\n".format(mode[0][0]))
			#f_2.write("-------------------------\n")
			#print("aps: " + str(aps_temp))
			#print("ap_n: " + ap_n)
			if ap_n in aps_temp:
				#f_2.write("****{},{}\n".format(aps_temp,ap_n))
				if str(sta.params['associatedTo'][wlan]) != str(ap_n):
					tiempo_final = time.time()
					time_selec = tiempo_final - tiempo_inicial
					"""
					f_2.write("**************************************SI Cambio de AP{}-------------------------\n".format(mode[0][0]))
					f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
					f_2.write("ap_n: {}, array_indice: {}, array_ap: {}, ap: {}\n".format(ap_n, indice, aps_temp[indice], sta.params['apsInRange'][indice]))
					f_2.write("-------------------------\n")
					"""
					#print("El AP - {} esta en la posicion {} de la lista".format(ap_n,indice))
					indice = aps_temp.index(str(ap_n))
					f= open("/home/mininet/Escritorio/scripts/output/rf.txt","a+")
					#f.write("{},{},{}\n".format(sta.name, str(sta.params['associatedTo'][wlan]),mrf))
					f.write('{"time":"%s","sta":"%s", "oldAp":"%s", "newAp":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s"}\n' %(str(time_selec*1000),str(sta.name),str(sta.params['associatedTo'][wlan]), str(sta.params['apsInRange'][indice]), str(aps_temp), str(sta.params['battery']), str(sta.params['position'])))
					#f.write('{"time":"%s", "sta":"%s", "apsInRange":"%s", "battery":"%s", "position": "%s", "oldAp":"%s", "newAp":"%s"}\n' %(str(time_selec*1000),str(sta.name), str(aps_temp), str(sta.params['battery']), str(sta.params['position']), str(sta.params['associatedTo'][wlan]), str(aps_temp[v_cer.argmax()])))
					debug('iw dev %s disconnect\n' % sta.params['wlan'][wlan])
					sta.pexec('iw dev %s disconnect' % sta.params['wlan'][wlan])
					Association.associate_infra(sta, sta.params['apsInRange'][indice], wlan=wlan, ap_wlan=ap_wlan)
					#sta.params['battery'] = sta.params['battery'] - 0.1
					sta.params['battery'] = sta.params['battery'] - (0.01 * sta.get_distance_to(sta.params['associatedTo'][wlan]))
					f.close()
				else:
					#f_2.write("-------------------------NO Cambio de AP{}-------------------------\n".format(mode[0][0]))
					print('misma red')
			#if ap_n in aps_temp:
			else:
				print('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write('*******AP NOOOO ESTA EN RANGO*******')
				#f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
				
			
			"""
			else:
			print('*******AP NOOOO ESTA EN RANGO*******')
			f_2.write('*******AP NOOOO ESTA EN RANGO*******')
			f_2.write("{},{}\n".format(str(sta.params['associatedTo'][wlan]),ap_n))
			"""
			
		#f_2.close()
		
		return self.changeAP
