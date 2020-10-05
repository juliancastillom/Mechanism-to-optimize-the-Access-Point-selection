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
	sta1 = net.addStation('sta1', ip='10.0.1.1', mac='00:00:00:00:09:01', position='90.0,150.0,0', range = 20, speed = 5, battery = 100)
	#AP1
	sta2 = net.addStation('sta2', ip='10.0.1.2', mac='00:00:00:00:09:02', position='70.0,170.0,0', range = 20, battery = 100)
	#sta2 = net.addStation('sta2', ip='10.0.0.9', range = 20)
	sta3 = net.addStation('sta3', ip='10.0.1.3', mac='00:00:00:00:09:03', position='110.0,125.0,0', range = 20, battery = 100)
	
	#AP3
	sta4 = net.addStation('sta4', ip='10.0.1.4', mac='00:00:00:00:09:04', position='90.0,140.0,0', range = 20, battery = 100)
	
	sta5 = net.addStation('sta5', ip='10.0.1.5', mac='00:00:00:00:09:05', position='50.0,115.0,0', range = 20, battery = 100)
	
	sta6 = net.addStation('sta6', ip='10.0.1.6', mac='00:00:00:00:09:06', position='90.0,100.0,0', range = 20, battery = 100)
	
	sta7 = net.addStation('sta7', ip='10.0.1.7', mac='00:00:00:00:09:07', position='80.0,150.0,0', range = 20, battery = 100)
	
	sta8 = net.addStation('sta8', ip='10.0.1.8', mac='00:00:00:00:09:08', position='130.0,140.0,0', range = 20, battery = 100)
	
	#AP4
	sta9 = net.addStation('sta9', ip='10.0.1.9', mac='00:00:00:00:09:09', position='90.0,140.0,0', range = 20, battery = 100)
	
	sta10 = net.addStation('sta10', ip='10.0.1.10', mac='00:00:00:00:09:10', position='90.0,140.0,0', range = 20, battery = 100)
	
	sta11 = net.addStation('sta11', ip='10.0.1.11', mac='00:00:00:00:09:11', position='90.0,140.0,0', range = 20, battery = 100)
	
	sta12 = net.addStation('sta12', ip='10.0.1.12', mac='00:00:00:00:09:12', position='90.0,150.0,0', range = 20, battery = 100)
	
	sta13 = net.addStation('sta13', ip='10.0.1.13', mac='00:00:00:00:09:13', position='90.0,150.0,0', range = 20, battery = 100)
	
	sta14 = net.addStation('sta14', ip='10.0.1.14', mac='00:00:00:00:09:14', position='48.0,145.0,0', range = 20, battery = 100)
	
	sta15 = net.addStation('sta15', ip='10.0.1.15', mac='00:00:00:00:09:15', position='48.0,145.0,0', range = 20, battery = 100)
	
	sta16 = net.addStation('sta16', ip='10.0.1.16', mac='00:00:00:00:09:16', position='135.0,145.0,0', range = 20, battery = 100)
	
	sta17 = net.addStation('sta17', ip='10.0.1.17', mac='00:00:00:00:09:17', position='120.0,145.0,0', range = 20, battery = 100)
	
	sta18 = net.addStation('sta18', ip='10.0.1.18', mac='00:00:00:00:09:18', position='140.0,150.0,0', range = 20, battery = 100)
	
	sta19 = net.addStation('sta19', ip='10.0.1.19', mac='00:00:00:00:09:19', position='90.0,100.0,0', range = 20, battery = 100)
	
	sta20 = net.addStation('sta20', ip='10.0.1.20', mac='00:00:00:00:09:20', position='90.0,125.0,0', range = 20, battery = 100)
	
	sta21 = net.addStation('sta21', ip='10.0.1.21', mac='00:00:00:00:09:21', position='90.0,91.0,0', range = 20, battery = 100)
	
	sta22 = net.addStation('sta22', ip='10.0.1.22', mac='00:00:00:00:09:22', position='91.0,186.0,0', range = 20, battery = 100)
	
	sta23 = net.addStation('sta23', ip='10.0.1.23', mac='00:00:00:00:09:23', position='91.0,186.0,0', range = 20, battery = 100)
	
	sta24 = net.addStation('sta24', ip='10.0.1.24', mac='00:00:00:00:09:24', position='91.0,186.0,0', range = 20, battery = 100)
	
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
	file_mov = "movimientos_entrenamientoV1.txt"
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
		sta11.setPosition("{}".format(line[11]))
		sta12.setPosition("{}".format(line[12]))
		
		sta13.setPosition("{}".format(line[13]))
		sta14.setPosition("{}".format(line[14]))
		sta15.setPosition("{}".format(line[15]))
		sta16.setPosition("{}".format(line[16]))
		
		sta17.setPosition("{}".format(line[17]))
		sta18.setPosition("{}".format(line[18]))
		sta19.setPosition("{}".format(line[19]))
		sta20.setPosition("{}".format(line[20]))
		
		sta21.setPosition("{}".format(line[21]))
		sta22.setPosition("{}".format(line[22]))
		sta23.setPosition("{}".format(line[23]))
		sta24.setPosition("{}".format(line[24]))
		
		print(line[0])
		#print(line[1])
		#print(line[2])
		
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
		
		for i in range( len(sta11.params["apsInRange"]) ):
			ap_temp = sta11.params['apsInRange'][i]
			rssi_aptemp = sta11.get_rssi(ap_temp,0,sta11.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta11.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta11.params["apsInRange"]) ):
				ap_temp2 = sta11.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta11.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta11.params['associatedTo'][0].name)))
			#f_sta11_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta11.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta11.params['associatedTo'][0].name, sta11.get_distance_to(sta11.params['associatedTo'][0])) )
		
		for i in range( len(sta12.params["apsInRange"]) ):
			ap_temp = sta12.params['apsInRange'][i]
			rssi_aptemp = sta12.get_rssi(ap_temp,0,sta12.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta12.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta12.params["apsInRange"]) ):
				ap_temp2 = sta12.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta12.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta12.params['associatedTo'][0].name)))
			#f_sta12_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta12.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta12.params['associatedTo'][0].name, sta12.get_distance_to(sta12.params['associatedTo'][0])) )
		
		for i in range( len(sta13.params["apsInRange"]) ):
			ap_temp = sta13.params['apsInRange'][i]
			rssi_aptemp = sta13.get_rssi(ap_temp,0,sta13.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta13.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta13.params["apsInRange"]) ):
				ap_temp2 = sta13.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta13.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta13.params['associatedTo'][0].name)))
			#f_sta13_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta13.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta13.params['associatedTo'][0].name, sta13.get_distance_to(sta13.params['associatedTo'][0])) )
		
		for i in range( len(sta14.params["apsInRange"]) ):
			ap_temp = sta14.params['apsInRange'][i]
			rssi_aptemp = sta14.get_rssi(ap_temp,0,sta14.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta14.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta14.params["apsInRange"]) ):
				ap_temp2 = sta14.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta14.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta14.params['associatedTo'][0].name)))
			#f_sta14_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta14.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta14.params['associatedTo'][0].name, sta14.get_distance_to(sta14.params['associatedTo'][0])) )
		
		for i in range( len(sta15.params["apsInRange"]) ):
			ap_temp = sta15.params['apsInRange'][i]
			rssi_aptemp = sta15.get_rssi(ap_temp,0,sta15.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta15.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta15.params["apsInRange"]) ):
				ap_temp2 = sta15.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta15.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta15.params['associatedTo'][0].name)))
			#f_sta15_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta15.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta15.params['associatedTo'][0].name, sta15.get_distance_to(sta15.params['associatedTo'][0])) )
		
		for i in range( len(sta16.params["apsInRange"]) ):
			ap_temp = sta16.params['apsInRange'][i]
			rssi_aptemp = sta16.get_rssi(ap_temp,0,sta16.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta16.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta16.params["apsInRange"]) ):
				ap_temp2 = sta16.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta16.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta16.params['associatedTo'][0].name)))
			#f_sta16_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta16.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta16.params['associatedTo'][0].name, sta16.get_distance_to(sta16.params['associatedTo'][0])) )
		
		for i in range( len(sta17.params["apsInRange"]) ):
			ap_temp = sta17.params['apsInRange'][i]
			rssi_aptemp = sta17.get_rssi(ap_temp,0,sta17.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta17.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta17.params["apsInRange"]) ):
				ap_temp2 = sta17.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta17.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta17.params['associatedTo'][0].name)))
			#f_sta17_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta17.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta17.params['associatedTo'][0].name, sta17.get_distance_to(sta17.params['associatedTo'][0])) )
		
		for i in range( len(sta18.params["apsInRange"]) ):
			ap_temp = sta18.params['apsInRange'][i]
			rssi_aptemp = sta18.get_rssi(ap_temp,0,sta18.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta18.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta18.params["apsInRange"]) ):
				ap_temp2 = sta18.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta18.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta18.params['associatedTo'][0].name)))
			#f_sta18_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta18.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta18.params['associatedTo'][0].name, sta18.get_distance_to(sta18.params['associatedTo'][0])) )
		
		for i in range( len(sta19.params["apsInRange"]) ):
			ap_temp = sta19.params['apsInRange'][i]
			rssi_aptemp = sta19.get_rssi(ap_temp,0,sta19.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta19.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta19.params["apsInRange"]) ):
				ap_temp2 = sta19.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta19.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta19.params['associatedTo'][0].name)))
			#f_sta19_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta19.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta19.params['associatedTo'][0].name, sta19.get_distance_to(sta19.params['associatedTo'][0])) )
		
		for i in range( len(sta20.params["apsInRange"]) ):
			ap_temp = sta20.params['apsInRange'][i]
			rssi_aptemp = sta20.get_rssi(ap_temp,0,sta20.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta20.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta20.params["apsInRange"]) ):
				ap_temp2 = sta20.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta20.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta20.params['associatedTo'][0].name)))
			#f_sta20_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta20.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta20.params['associatedTo'][0].name, sta20.get_distance_to(sta20.params['associatedTo'][0])) )
		
		for i in range( len(sta21.params["apsInRange"]) ):
			ap_temp = sta21.params['apsInRange'][i]
			rssi_aptemp = sta21.get_rssi(ap_temp,0,sta21.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta21.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta21.params["apsInRange"]) ):
				ap_temp2 = sta21.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta21.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta21.params['associatedTo'][0].name)))
			#f_sta21_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta21.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta21.params['associatedTo'][0].name, sta21.get_distance_to(sta21.params['associatedTo'][0])) )
		
		for i in range( len(sta22.params["apsInRange"]) ):
			ap_temp = sta22.params['apsInRange'][i]
			rssi_aptemp = sta22.get_rssi(ap_temp,0,sta22.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta22.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta22.params["apsInRange"]) ):
				ap_temp2 = sta22.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta22.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta22.params['associatedTo'][0].name)))
			#f_sta22_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta22.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta22.params['associatedTo'][0].name, sta22.get_distance_to(sta22.params['associatedTo'][0])) )
		
		for i in range( len(sta23.params["apsInRange"]) ):
			ap_temp = sta23.params['apsInRange'][i]
			rssi_aptemp = sta23.get_rssi(ap_temp,0,sta23.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta23.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta23.params["apsInRange"]) ):
				ap_temp2 = sta23.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta23.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta23.params['associatedTo'][0].name)))
			#f_sta23_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta23.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta23.params['associatedTo'][0].name, sta23.get_distance_to(sta23.params['associatedTo'][0])) )
		
		for i in range( len(sta24.params["apsInRange"]) ):
			ap_temp = sta24.params['apsInRange'][i]
			rssi_aptemp = sta24.get_rssi(ap_temp,0,sta24.get_distance_to(ap_temp))
			n_est_aptemp = len(ap_temp.params['associatedStations'])
			dis_to_aptemp = sta24.get_distance_to(ap_temp)
			bat_temp = 0.01 * dis_to_aptemp
			aps = ""
			for n in range( len(sta24.params["apsInRange"]) ):
				ap_temp2 = sta24.params['apsInRange'][n]
				aps = aps + ap_temp2.name
			f_datos_entrenamiento.write("{},{},{},{},{},{},{},{}\n".format(str(sta24.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta24.params['associatedTo'][0].name)))
			#f_sta24_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta24.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta24.params['associatedTo'][0].name, sta24.get_distance_to(sta24.params['associatedTo'][0])) )
		
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

