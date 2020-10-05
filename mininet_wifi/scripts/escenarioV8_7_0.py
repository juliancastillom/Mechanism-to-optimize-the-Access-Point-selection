#!/usr/bin/python
#creado 24_jun_2019
#se recorre un txt con coordenadas para varios dispositivos
#Creado para sacer los datos de cada movimiento de la estacion 1
#Se realiza PRUEBA IPERF: Se crean dos terminales, uno para servidor iperf(sta5) y otro un cliente(sta1)

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
	#asoc = "topsis"
	#asoc = "saw"
	asoc = "rf"
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
	
	info( '*** Add switches/APs\n')
	ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='n', channel='1', position='50.0,150.0,0', antennaGain = 5, range = 45, battery = 100, maxDis = 15) # gain 8 = (txpow = 3 + gain = 5)
	ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='n', channel='7', position='90.0,180.0,0', antennaGain = 6, range = 50, battery = 100, maxDis = 18)# gain 3 = ( gain = 3)
	ap3 = net.addAccessPoint('ap3', ssid='ap3-ssid', mode='n', channel='11', position='130.0,150.0,0', antennaGain = 5, range=45, battery = 100, maxDis = 15) # gain 7 = (txpow = 2 + gain = 5)
	ap4 = net.addAccessPoint('ap4', ssid='ap4-ssid', mode='n', channel='11', position='90.0,90.0,0', antennaGain = 6, range=57, battery = 100, maxDis = 20) # gain 10 = (txpow = 4 + gain = 6)
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
	sta1 = net.addStation('sta1', ip='10.0.1.123', mac='00:00:00:00:09:01', position='40.48,100.36,0.00', range = 20, speed = 5, battery = 100, hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","","","","","",""]])
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
	sta2 = net.addStation('sta2', ip='10.0.1.2', mac='00:00:00:00:09:02', position='30.0,180.0,0', range = 20, battery = 100, app = 2, hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","","","","","",""]])
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
	#print sta2.cmd('touch sta_output/sta2_file.txt') #Crear archivo automaticamente
	#print sta2.cmd('python aleat.py')
	#print sta2.cmd('python aleat.py &')
	

	#Prueba iperf
	print("creando terminales")
	makeTerm( sta5, cmd="bash -c 'iperf -s -u -p 5566 -i 1 > resultiperf_sta1;'" )
	#makeTerm( sta9, cmd="bash -c 'iperf -s -u -p 5566 -i 1 > resultiperf_sta2;'" )
	time.sleep(1)
	makeTerm( sta1, cmd="bash -c 'iperf -c 10.0.1.5 -u -b 1M -t 600 -p 5566;'" )
	#makeTerm( sta2, cmd="bash -c 'iperf -c 10.0.1.9 -u -b 2M -t 1000 -p 5566;'" )
	print("terminales creandos")

	
	#replayingMobility(net)
	
	#Movimiento de una estacion de acuerdo a un txt con las coordenadas
	#file_mov = "u10_1_mov.txt"
	file_mov = "u10_mov.txt"
	#file_mov = "movimientos_entrenamientoV2.txt"
	mov1 = open(file_mov, 'r')
	raw_data = mov1.readlines()
	mov1.close()
	
	f_sta1_info= open("output/sta1_info.txt","w+")
	f_sta1_info.write('{},{},{},{},{},{},{},{}\n'.format("station", "associatedTo","time","battery", "rssi", "x","y","z"))
	
	#sta1_his2 = [[0, 0, 0],[0, 0, 0],["","",""]]
	print(sta1.params.get("hist"))
	
	for data in raw_data:
		line = data.split()
		sta1.setPosition("{}".format(line[1]))
		#sta2.setPosition("{}".format(line[2]))
		print(line[0])
		"""
		nodes = net.stations
		print("--------------------------")
		#print(nodes)
		for node in nodes:
			print(node.name)
		print("--------------------------")
		"""
		#sta1_ap = sta1.params.get("associatedTo", "")
		
		"""
		var = sta1.params.get("associatedTo", "null")[0]
		print var
		print(str(type(var)))
		
		hist = sta1.params.get("hist")
		
		if type(var) == str:
			del hist[2][0]
			print(hist)
			hist[2].append("")
			print(hist)
			print("es " + str(type(var)))
		else:
			del hist[2][0]
			print(hist)
			hist[2].append(var.name)
			print(hist)
			print("NO, es " + str(type(var)))
		"""
		"""
		aps_in_range_name = []
		aps_in_range_rssi = []
		for n in range( len(sta1.params["apsInRange"]) ):
			ap_temp2 = sta1.params['apsInRange'][n]
			
			ap_temp2 = sta1.params['apsInRange'][n]
			aps_in_range_name.append(ap_temp2.name)
			
			rssi_aptemp = sta1.get_rssi(ap_temp2,0,sta1.get_distance_to(ap_temp2))
			aps_in_range_rssi.append(rssi_aptemp)
		print(aps_in_range_name)
		print(aps_in_range_rssi)
		#print(max(aps_in_range_rssi))
		indice = aps_in_range_rssi.index(max(aps_in_range_rssi))
		
		maximo = max(aps_in_range_rssi)
		
		#print (indice)
		#print (maximo)
		n=0
		#print(len(hist_rssi))
		for i in aps_in_range_rssi:
			if maximo == i:
				#print n
				print(aps_in_range_rssi[n])
				print(aps_in_range_name[n])
				#print (i)
			n = n+1
		#aps = aps + ap_temp2.name[2:]
		"""
		
		"""
		print("--------sta2---")
		
		hist2 = sta2.params.get("hist", "null")
		
		if hist2 != "null":
			print("con hist")
			var2 = sta2.params.get("associatedTo", "null")[0]
			print var2
			print(str(type(var2)))
			
			if type(var2) == str:
				del hist2[2][0]
				print(hist2)
				hist2[2].append("")
				print(hist2)
				print("es " + str(type(var2)))
			else:
				del hist2[2][0]
				print(hist2)
				hist2[2].append(var2.name)
				print(hist2)
				print("NO, es " + str(type(var2)))
		else:
			print("sin hist")
		"""
		#print(line[1])
		#print(line[2])
		#print(sta1.params.get("name", 1))
		#print(sta1.params.get("associatedTo", 2))
		
		f_sta1_info.write('{},{},{},{},{},{},{},{}\n'.format( str(sta1.name), str(sta1.params.get('associatedTo')[0]), str(int(round(time.time() * 1000))), str(sta1.params['battery']), str(sta1.params['rssi']), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2] ) )
		#f_sta1_info.write('{},{},{},{},{},{},{},{}\n'.format( str(sta1.name), str(sta1.params['associatedTo']), str(int(round(time.time() * 1000))), str(sta1.params['battery']), str(sta1.params['rssi']), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2] ) )
		
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
			f_ml.write("{},{},{},{},{},{},{},{}\n".format(str(sta1.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta1.params['associatedTo'][0].name)))
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
			f_ml.write("{},{},{},{},{},{},{},{}\n".format(str(sta2.name), str(aps), str(ap_temp.name), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta1.params['associatedTo'][0].name)))
			#f_sta1_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta1.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta1.params['associatedTo'][0].name, sta1.get_distance_to(sta1.params['associatedTo'][0])) )
		"""
		
		time.sleep(0.20)
	
	f_sta1_info.close()
	
	#time.sleep(50)
	
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

