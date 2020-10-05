#!/usr/bin/python
#creado 11_jul_2019
#se recorre un txt con coordenadas para varios dispositivos
#Creado para extraer graficas de throughtpu
#Se mueven dos estaciones, una con un movimiento lineal y otra con random_walk

from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station, OVSKernelAP
from mn_wifi.cli import CLI_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from subprocess import call
from mininet.link import TCLink
import sys
import os
from replay import replayingMobility
from replay import replayingMobility2
import time
from mn_wifi.associationControl import associationControl
from mininet.term import cleanUpScreens, makeTerm


def myNetwork():
	#net = Mininet_wifi(controller=RemoteController, link=TCLink )
	#net = Mininet_wifi(link=TCLink, xterms=True ) # abre todas las terminales de los dispositivos
	net = Mininet_wifi(link=TCLink )
	info( '*** Adding controller\n' )
	#c0=net.addController(name='c0', controller=RemoteController, ip='10.0.2.15', port=6633 )
	c0=net.addController(name='c0', controller=Controller, protocol='tcp', port=6633)
	
	#asoc = "ssf"
	#asoc = "llf"
	#asoc = "llf2"
	#asoc = "slf"
	asoc = "topsis"
	#asoc = "saw"
	#asoc = "rf"
	#asoc = "dl"
	
	if asoc == "ssf":
		f_ssf= open("/home/mininet/Escritorio/scripts/output/ssf.txt","w+")
		f_ssf.close()
	elif asoc == "llf":
		f_llf= open("/home/mininet/Escritorio/scripts/output/llf.txt","w+")
		f_llf.close()
	elif asoc == "slf":
		f_slf= open("/home/mininet/Escritorio/scripts/output/slf.txt","w+")
		f_slf.close()
	elif asoc == "topsis":
		f_topsis= open("/home/mininet/Escritorio/scripts/output/topsis.txt","w+")
		f_topsis.close()
	elif asoc == "saw":
		f_topsis= open("/home/mininet/Escritorio/scripts/output/saw.txt","w+")
		f_topsis.close()
	elif asoc == "rf":
		f_rf= open("/home/mininet/Escritorio/scripts/output/rf.txt","w+")
		f_rf.close()
	elif asoc == "dl":
		f_rf= open("/home/mininet/Escritorio/scripts/output/dl.txt","w+")
		f_rf.close()
	
	f_datosML3= open("/home/mininet/Escritorio/scripts/output/datosML3.txt","w+")
	f_datosML3.write("{},{},{},{},{},{},{}\n".format("station", "ap", "rssi", "num_sta", "dist", "cons_bat", "associatedTo"))
	f_datosML3.close()
	
	f_datosML4= open("/home/mininet/Escritorio/scripts/output/datosML4.txt","w+")
	f_datosML4.write("{},{},{},{},{},{},{}\n".format("station","aps", "ap", "rssi", "num_sta", "dist", "cons_bat", "associatedTo"))
	f_datosML4.close()
	
	f_datosML5= open("/home/mininet/Escritorio/scripts/output/datosML5.txt","w+")
	f_datosML5.write("{},{},{},{},{},{},{}\n".format("station","aps", "ap", "rssi", "num_sta", "dist", "cons_bat", "associatedTo"))
	f_datosML5.close()
	
	f_datos_entrenamiento= open("/home/mininet/Escritorio/scripts/output/datos_entrenamiento.txt","w+")
	f_datos_entrenamiento.write("{},{},{},{},{},{},{}\n".format("station","aps", "ap", "rssi", "num_sta", "dist", "cons_bat", "associatedTo"))
	#f_datos_entrenamiento.close()
	
	info( '*** Add switches/APs\n')
	ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='n', channel='1', position='50.0,150.0,0', antennaGain = 5, range = 45, battery = 100) # gain 8 = (txpow = 3 + gain = 5)
	ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='n', channel='7', position='90.0,180.0,0', antennaGain = 6, range = 50, battery = 100)# gain 3 = ( gain = 3)
	ap3 = net.addAccessPoint('ap3', ssid='ap3-ssid', mode='n', channel='11', position='130.0,150.0,0', antennaGain = 5, range=45, battery = 100) # gain 7 = (txpow = 2 + gain = 5)
	ap4 = net.addAccessPoint('ap4', ssid='ap4-ssid', mode='n', channel='11', position='90.0,90.0,0', antennaGain = 6, range=57, battery = 100) # gain 10 = (txpow = 4 + gain = 6)
	s1 = net.addSwitch('s1')

	info( '*** Add hosts/stations\n')
	
	
	u1_d1 = net.addStation('u1_d1', ip='10.0.0.134', mac='01:01:01:00:01:01', position='10.0,150.0,0', range = 20, speed = 1, battery = 100)
	u1_d2 = net.addStation('u1_d2', ip='10.0.0.2', mac='02:01:02:00:01:02', position='10.0,150.0,0', range = 20, speed = 1, battery = 100)
	u1_d3 = net.addStation('u1_d3', ip='10.0.0.3', mac='03:01:03:00:01:03', position='10.0,150.0,0', range = 20, speed = 1, battery = 100)
	
	u2_d1 = net.addStation('u2_d1', ip='10.0.0.4', mac='01:02:01:00:02:01', position='90.0,210.0,0', range = 20, speed = 2, battery = 100)
	u2_d2 = net.addStation('u2_d2', ip='10.0.0.5', mac='02:02:02:00:02:02', position='90.0,210.0,0', range = 20, speed = 2, battery = 100)
	u2_d3 = net.addStation('u2_d3', ip='10.0.0.6', mac='03:02:03:00:02:03', position='90.0,210.0,0', range = 20, speed = 2, battery = 100)
	u2_d4 = net.addStation('u2_d4', ip='10.0.0.7', mac='04:02:04:00:02:04', position='90.0,210.0,0', range = 20, speed = 2, battery = 100)
	
	#AP2
	sta1 = net.addStation('sta1', ip='10.0.1.123', mac='00:00:00:00:09:01', position='32.0,112.0,0', range = 20, speed = 5, battery = 100)
	sta8 = net.addStation('sta8', ip='10.0.1.8', mac='00:00:00:00:09:08', position='91.0,175.0,0', range = 20, battery = 100)
	
	#AP4
	sta9 = net.addStation('sta9', ip='10.0.1.9', mac='00:00:00:00:09:09', position='75.0,75.0,0', range = 20, battery = 100)
	sta10 = net.addStation('sta10', ip='10.0.1.10', mac='00:00:00:00:09:10', position='35.0,95.0,0', range = 20, battery = 100)
	
	#AP3
	sta4 = net.addStation('sta4', ip='10.0.1.4', mac='00:00:00:00:09:04', position='125.0,110.0,0', range = 20, battery = 100)
	sta5 = net.addStation('sta5', ip='10.0.1.5', mac='00:00:00:00:09:05', position='90.0,70.0,0', range = 20, battery = 100)
	sta6 = net.addStation('sta6', ip='10.0.1.6', mac='00:00:00:00:09:06', position='125.0,180.0,0', range = 20, battery = 100)
	sta7 = net.addStation('sta7', ip='10.0.1.7', mac='00:00:00:00:09:07', position='110.0,170.0,0', range = 20, battery = 100)
	
	#AP1
	sta2 = net.addStation('sta2', ip='10.0.1.2', mac='00:00:00:00:09:02', position='30.0,180.0,0', range = 20, battery = 100)
	#sta2 = net.addStation('sta2', ip='10.0.0.9', range = 20)
	sta3 = net.addStation('sta3', ip='10.0.1.3', mac='00:00:00:00:09:03', position='50.0,125.0,0', range = 20, battery = 100)
	
	h1 = net.addHost( 'h1', ip='10.0.2.123', mac='00:00:00:00:10:01', battery = 100)

	info("*** Configuring Propagation Model\n")
	#net.setPropagationModel(model="logDistance", exp=3)

	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	#net.setChannelEquation(bw='5', loss='0.04', delay='0', latency='0')

	info( '*** Add links\n')

	net.addLink(s1, ap1)
	net.addLink(s1, ap2)
	net.addLink(s1, ap3)
	net.addLink(s1, ap4)
	
	net.addLink(s1, h1)
	
	net.plotGraph(max_x=180, max_y=250)
	
	print "*** Enabling association control (AP)"
	
	net.setAssociationCtrl( asoc )
	
	#Asignar el recorrido del dispositivo teniendo en cuenta un archivo con las coordenadas
	#Para habilitar --> Uncomment >> replayingMobility(net)
	"""
	getTrace(u1_d1, 'u1_mov.txt')
	getTrace(u1_d2, 'u1_mov.txt')
	getTrace(u1_d3, 'u1_mov.txt')
	
	getTrace(u2_d1, 'u2_mov.txt')
	getTrace(u2_d2, 'u2_mov.txt')
	getTrace(u2_d3, 'u2_mov.txt')
	getTrace(u2_d4, 'u2_mov.txt')
	"""
	
	#getTrace(sta1, 'u5_mov.txt')   #Uncomment >> replayingMobility(net) --> and comment net.plotGraph(max_x=180, max_y=250)
	"""
	print("detenido")
	time.sleep(18)
	print("inicia mov")
	"""
	info( '*** Starting network\n')
	net.build()
	net.start()
	
	ap1.setTxPower(3, intf='ap1-wlan1')
	ap2.setTxPower(4, intf='ap2-wlan1')
	ap3.setTxPower(2, intf='ap3-wlan1')
	ap4.setTxPower(4, intf='ap4-wlan1')
	
	#------------------Iperf before configure BW------------------------
	#print('\n---- Iperf before configure BW ----\n')
	#iperfTest()
	
	#------------------BW Configurarion---------------------------------
	"""
	print('\n---- IoT Device 1 ---- \n  ~~~~ Command to limit bandwidth ~~~~\n    .... wondershaper sta1-wlan0 2048 1024 ....')
	print sta1.cmd('wondershaper sta1-wlan0 2048 1024')
	print sta1.cmd('touch sta_output/sta1_file.txt') #Crear archivo automaticamene
	
	print('\n---- IoT device 2 ---- \n  ~~~~ Command to limit bandwidth ~~~~\n    .... wondershaper sta2-wlan0 1024 512 ....')
	print sta2.cmd('wondershaper sta2-wlan0 1024 512')
	print sta2.cmd('pwd')
	"""
	
	#PRUEBA IPERF
	"""
	print("creando terminales")
	makeTerm( sta5, cmd="bash -c 'iperf -s -u -p 5566 -i 1 > resultiperf_sta1;'" )
	makeTerm( sta9, cmd="bash -c 'iperf -s -u -p 5566 -i 1 > resultiperf_sta2;'" )
	time.sleep(1)
	makeTerm( sta1, cmd="bash -c 'iperf -c 10.0.1.5 -u -b 2M -t 1000 -p 5566;'" )
	makeTerm( sta2, cmd="bash -c 'iperf -c 10.0.1.9 -u -b 2M -t 1000 -p 5566;'" )
	print("terminales creandos")
	#print sta2.cmd('touch sta_output/sta2_file.txt') #Crear archivo automaticamente
	#print sta2.cmd('python aleat.py')
	#print sta2.cmd('python aleat.py &')
	"""
	
	#replayingMobility(net)
	
	#------------------Iperf after configure BW-------------------------
	
	print('---- Iperf after configure BW ----\n')
	#net.iperf((sta1, h1))
	#net.iperf((h1, sta1))
	
	
	#Movimiento de una estacion de acuerdo a un txt con las coordenadas
	file_mov = "movimientos_entrenamiento.txt"
	mov1 = open(file_mov, 'r')
	raw_data = mov1.readlines()
	mov1.close()
	f_sta1= open("output/sta1_params.txt","w+")
	f_sta1_data= open("output/stas_params_data.txt","w+")
	f_sta_info= open("output/stas_params_info.txt","w+")
	f_ap1= open("output/ap1_params.txt","w+")
	f_ap2= open("output/ap2_params.txt","w+")
	f_ap3= open("output/ap3_params.txt","w+")
	f_ap4= open("output/ap4_params.txt","w+")
	f_ml= open("/home/mininet/Escritorio/scripts/output/datosML2.txt","w+")
	f_ml.write("{},{},{},{},{},{},{},{}\n".format("station", "aps_range", "ap", "rssi", "num_sta", "dist", "cons_bat", "associatedTo"))
	f_sta_info.write('{},{},{},{},{}\n'.format("station","time","x","y","z"))
	
	for data in raw_data:
		line = data.split()
		sta1.setPosition("{}".format(line[1]))
		sta2.setPosition("{}".format(line[2]))
		sta3.setPosition("{}".format(line[3]))
		sta4.setPosition("{}".format(line[4]))
		
		sta5.setPosition("{}".format(line[5]))
		sta6.setPosition("{}".format(line[6]))
		sta7.setPosition("{}".format(line[7]))
		sta8.setPosition("{}".format(line[8]))
		
		sta9.setPosition("{}".format(line[9]))
		sta10.setPosition("{}".format(line[10]))
		#sta11.setPosition("{}".format(line[3]))
		#sta12.setPosition("{}".format(line[3]))
		
		print(line[0])
		#print(line[1])
		#print(line[2])
		
		"""
		f_sta1.write( '[' + str(int(round(time.time() * 1000))) + ",")
		f_sta1.write(str(line[0]) + ",")
		f_sta1.write(str(sta1.params['apsInRange']) + ",")
		f_sta1.write(str(sta1.params['associatedTo']) + ",")
		f_sta1.write(str(sta1.params['rssi']) + ",")
		f_sta1.write(str(sta1.params['position']) + ",")
		f_sta1.write(str(sta1.params['mac']) + "]\n\n")
		
		f_sta_info.write('{},{},{},{},{}\n'.format( str(sta1.name), str(int(round(time.time() * 1000))), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2] ) )
		"""
		
		
		for i in range( len(sta1.params["apsInRange"]) ):
			ap_temp = sta1.params['apsInRange'][i]
			rssi_aptemp = sta1.get_rssi(ap_temp,0,sta1.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta1.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta1.params["apsInRange"]) ):
				ap_temp2 = sta1.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta1.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta1.params['associatedTo'][0].name)))
			#f_sta1_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta1.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta1.params['associatedTo'][0].name, sta1.get_distance_to(sta1.params['associatedTo'][0])) )
		
		for i in range( len(sta2.params["apsInRange"]) ):
			ap_temp = sta2.params['apsInRange'][i]
			rssi_aptemp = sta2.get_rssi(ap_temp,0,sta2.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta2.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta2.params["apsInRange"]) ):
				ap_temp2 = sta2.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta2.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta2.params['associatedTo'][0].name)))
			#f_sta1_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta1.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta1.params['associatedTo'][0].name, sta1.get_distance_to(sta1.params['associatedTo'][0])) )
		
		for i in range( len(sta3.params["apsInRange"]) ):
			ap_temp = sta3.params['apsInRange'][i]
			rssi_aptemp = sta3.get_rssi(ap_temp,0,sta3.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta3.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta3.params["apsInRange"]) ):
				ap_temp3 = sta3.params['apsInRange'][n]
				aps = aps + ap_temp3.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta3.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta3.params['associatedTo'][0].name)))
			#f_sta1_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta1.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta1.params['associatedTo'][0].name, sta1.get_distance_to(sta1.params['associatedTo'][0])) )
		
		for i in range( len(sta4.params["apsInRange"]) ):
			ap_temp = sta4.params['apsInRange'][i]
			rssi_aptemp = sta4.get_rssi(ap_temp,0,sta4.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta4.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta4.params["apsInRange"]) ):
				ap_temp2 = sta4.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta4.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta4.params['associatedTo'][0].name)))
			#f_sta4_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta4.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta4.params['associatedTo'][0].name, sta4.get_distance_to(sta4.params['associatedTo'][0])) )
		
		for i in range( len(sta5.params["apsInRange"]) ):
			ap_temp = sta5.params['apsInRange'][i]
			rssi_aptemp = sta5.get_rssi(ap_temp,0,sta5.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta5.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta5.params["apsInRange"]) ):
				ap_temp2 = sta5.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta5.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta5.params['associatedTo'][0].name)))
		
		for i in range( len(sta6.params["apsInRange"]) ):
			ap_temp = sta6.params['apsInRange'][i]
			rssi_aptemp = sta6.get_rssi(ap_temp,0,sta6.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta6.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta6.params["apsInRange"]) ):
				ap_temp2 = sta6.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta6.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta6.params['associatedTo'][0].name)))
		
		
		for i in range( len(sta7.params["apsInRange"]) ):
			ap_temp = sta7.params['apsInRange'][i]
			rssi_aptemp = sta7.get_rssi(ap_temp,0,sta7.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta7.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta7.params["apsInRange"]) ):
				ap_temp2 = sta7.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta7.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta7.params['associatedTo'][0].name)))
		
		
		for i in range( len(sta8.params["apsInRange"]) ):
			ap_temp = sta8.params['apsInRange'][i]
			rssi_aptemp = sta8.get_rssi(ap_temp,0,sta8.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta8.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta8.params["apsInRange"]) ):
				ap_temp2 = sta8.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta8.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta8.params['associatedTo'][0].name)))
		
		
		for i in range( len(sta9.params["apsInRange"]) ):
			ap_temp = sta9.params['apsInRange'][i]
			rssi_aptemp = sta9.get_rssi(ap_temp,0,sta9.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta9.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta9.params["apsInRange"]) ):
				ap_temp2 = sta9.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta9.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta9.params['associatedTo'][0].name)))
		
		
		for i in range( len(sta10.params["apsInRange"]) ):
			ap_temp = sta10.params['apsInRange'][i]
			rssi_aptemp = sta10.get_rssi(ap_temp,0,sta10.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta10.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta10.params["apsInRange"]) ):
				ap_temp2 = sta10.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta10.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta10.params['associatedTo'][0].name)))
		
		
		
		"""
		f_ap1.write( '[' + str(int(round(time.time() * 1000))) + ",")
		f_ap1.write(str(line[0]) + ",")
		f_ap1.write(str(ap1.params['stationsInRange']) + ",")
		f_ap1.write(str(ap1.params['associatedStations']) + ",")
		f_ap1.write(str(ap1.params['mac']) + ",")
		f_ap1.write(str(ap1.params['position']) + ",")
		f_ap1.write(str(ap1.params['range']) + ",")
		f_ap1.write(str(ap1.params['channel']) + ",")
		f_ap1.write(str(ap1.params['freq']) + ",")
		f_ap1.write(str(ap1.params['antennaGain']) + "]\n\n")
		
		f_ap2.write( '[' + str(int(round(time.time() * 1000))) + ",")
		f_ap2.write(str(line[0]) + ",")
		f_ap2.write(str(ap2.params['stationsInRange']) + ",")
		f_ap2.write(str(ap2.params['associatedStations']) + ",")
		f_ap2.write(str(ap2.params['mac']) + ",")
		f_ap2.write(str(ap2.params['position']) + ",")
		f_ap2.write(str(ap2.params['range']) + ",")
		f_ap2.write(str(ap2.params['channel']) + ",")
		f_ap2.write(str(ap2.params['freq']) + ",")
		f_ap2.write(str(ap2.params['antennaGain']) + "]\n\n")
		
		f_ap3.write( '[' + str(int(round(time.time() * 1000))) + ",")
		f_ap3.write(str(line[0]) + ",")
		f_ap3.write(str(ap3.params['stationsInRange']) + ",")
		f_ap3.write(str(ap3.params['associatedStations']) + ",")
		f_ap3.write(str(ap3.params['mac']) + ",")
		f_ap3.write(str(ap3.params['position']) + ",")
		f_ap3.write(str(ap3.params['range']) + ",")
		f_ap3.write(str(ap3.params['channel']) + ",")
		f_ap3.write(str(ap3.params['freq']) + ",")
		f_ap3.write(str(ap3.params['antennaGain']) + "]\n\n")
		
		f_ap4.write( '[' + str(int(round(time.time() * 1000))) + ",")
		f_ap4.write(str(line[0]) + ",")
		f_ap4.write(str(ap4.params['stationsInRange']) + ",")
		f_ap4.write(str(ap4.params['associatedStations']) + ",")
		f_ap4.write(str(ap4.params['mac']) + ",")
		f_ap4.write(str(ap4.params['position']) + ",")
		f_ap4.write(str(ap4.params['range']) + ",")
		f_ap4.write(str(ap4.params['channel']) + ",")
		f_ap4.write(str(ap4.params['freq']) + ",")
		f_ap4.write(str(ap4.params['antennaGain']) + "]\n\n")
		"""
		#time.sleep(0.05)
	
	f_sta1.close()
	f_sta1_data.close()
	f_ap1.close()
	f_ap2.close()
	f_ap3.close()
	f_ap4.close()
	f_ml.close()
	f_sta_info.close()
	f_datos_entrenamiento.close()
	
	print "*** Running CLI"
	info( '*** Post configure nodes\n')
	CLI_wifi(net)
	net.stop()

def getTrace(sta, file_):

	file_ = open(file_, 'r')
	raw_data = file_.readlines()
	file_.close()
	sta.position = []
	for data in raw_data:
		line = data.split()
		sta.position.append(line[1])
		
def iperfTest():
	"""net.iperf((sta1, sta2))
	net.iperf((sta1, sta3))
	net.iperf((sta1, sta4))
	
	net.iperf((sta2, sta1))
	net.iperf((sta2, sta3))
	net.iperf((sta2, sta4))
	
	net.iperf((sta1, h1))
	net.iperf((h1, sta1))
	
	net.iperf((sta2, h1))
	net.iperf((h1, sta2))
	
	net.iperf((sta3, h1))
	net.iperf((h1, sta3))
	
	net.iperf((h1, sta4))
	
	net.iperf((sta3, sta4))"""



if __name__ == '__main__':
	setLogLevel( 'info' )
	myNetwork()

