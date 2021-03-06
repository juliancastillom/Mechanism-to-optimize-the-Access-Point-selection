#!/usr/bin/python
#creado 23_may_2019
#Se crea una nueva funcion para recorrer el doc con las coordenadas...
#...con base a esas coordenadas se hace el recorrido de la estacion

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
	
	f_datosML3= open("/home/mininet/Escritorio/scripts/output/datosML3.txt","w+")
	f_datosML3.write("{},{},{},{},{},{},{}\n".format("station", "ap", "rssi", "num_sta", "dist", "cons_bat", "associatedTo"))
	f_datosML3.close()
	
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
	#net.setAssociationCtrl( 'ssf' )   
	#net.setAssociationCtrl( 'ssf2' )   
	#net.setAssociationCtrl( 'llf' )   
	#net.setAssociationCtrl( 'llf2' )   
	#net.setAssociationCtrl( 'slf' )  
	#net.setAssociationCtrl( 'slf2' )
	#net.setAssociationCtrl( 'topsis' )
	net.setAssociationCtrl( asoc )
	
	
	#RECORRIDOS LINEALES
	"""
	u1_start = '10.0,150.0,0'
	u1_stop = '160.0,170.0,0'
	
	u2_start = '25.0,70.0,0'
	u2_stop = '90.0,150.0,0'
	
	
	net.startMobility( time=0, repetitions=3, AC='ssf')
	
	net.mobility( u1_d1, 'start', time=1, position= u1_start)
	net.mobility( u1_d1, 'stop', time=29, position= u1_stop)
	
	net.mobility( u1_d2, 'start', time=1, position= u1_start)
	net.mobility( u1_d2, 'stop', time=29, position= u1_stop)
	
	net.mobility( u1_d3, 'start', time=1, position= u1_start)
	net.mobility( u1_d3, 'stop', time=29, position= u1_stop)
	
	#net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, seed=20)
	
	net.stopMobility( time=30 )
	"""
	
	"""
	sta1_start = '50.0,150.0,0'
	sta1_stop = '150.0,150.0,0'
	
	
	net.startMobility( time=10)
	
	net.mobility( sta1, 'start', time=11, position= sta1_start)
	net.mobility( sta1, 'stop', time=20, position= sta1_stop)
	
	#net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, seed=20)
	
	net.stopMobility( time=15 )
	"""
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
	print('\n---- IoT Device 1 ---- \n  ~~~~ Command to limit bandwidth ~~~~\n    .... wondershaper sta1-wlan0 2048 1024 ....')
	print sta1.cmd('wondershaper sta1-wlan0 2048 1024')
	print sta1.cmd('touch sta_output/sta1_file.txt') #Crear archivo automaticamene
	
	print('\n---- IoT device 2 ---- \n  ~~~~ Command to limit bandwidth ~~~~\n    .... wondershaper sta2-wlan0 1024 512 ....')
	print sta2.cmd('wondershaper sta2-wlan0 1024 512')
	print sta2.cmd('pwd')
	#print sta2.cmd('touch sta_output/sta2_file.txt') #Crear archivo automaticamente
	#print sta2.cmd('python aleat.py')
	#print sta2.cmd('python aleat.py &')
	
	
	#replayingMobility(net)
	
	#------------------Iperf after configure BW-------------------------
	
	print('---- Iperf after configure BW ----\n')
	#net.iperf((sta1, h1))
	#net.iperf((h1, sta1))
	
	
	#Movimiento de una estacion de acuerdo a un txt con las coordenadas
	file_mov = "u6_mov.txt"
	mov1 = open(file_mov, 'r')
	raw_data = mov1.readlines()
	mov1.close()
	f_sta1= open("output/sta1_params.txt","w+")
	f_sta1_data= open("output/sta1_params_data.txt","w+")
	f_ap1= open("output/ap1_params.txt","w+")
	f_ap2= open("output/ap2_params.txt","w+")
	f_ap3= open("output/ap3_params.txt","w+")
	f_ap4= open("output/ap4_params.txt","w+")
	f_ml= open("/home/mininet/Escritorio/scripts/output/datosML2.txt","w+")
	f_ml.write("{},{},{},{},{},{},{}\n".format("station", "ap", "rssi", "num_sta", "dist", "cons_bat", "associatedTo"))
	
	for data in raw_data:
		line = data.split()
		sta1.setPosition("{}".format(line[1]))
		#sta1.params['battery'] = sta1.params['battery'] - 1
		#print("node: %s - battery: %s" % (sta1.name, str(sta1.params['battery'])))
		#print('Time mov ' + time.strftime("%H:%M:%S") )
		#print('Time mov milliseconds' + str(int(round(time.time() * 1000))) )
		#print('Time mov milliseconds 2 ' + str(time.time()) )
		print(line[1])
		
		f_sta1.write( '[' + str(int(round(time.time() * 1000))) + ",")
		f_sta1.write(str(line[0]) + ",")
		f_sta1.write(str(sta1.params['apsInRange']) + ",")
		f_sta1.write(str(sta1.params['associatedTo']) + ",")
		f_sta1.write(str(sta1.params['rssi']) + ",")
		f_sta1.write(str(sta1.params['position']) + ",")
		f_sta1.write(str(sta1.params['mac']) + "]\n\n")
		
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
			f_ml.write("{},{},{},{},{},{},{}\n".format(str(sta1.name), str(aps), str(rssi_aptemp), str(n_est_aptemp), str(dis_to_aptemp), str(bat_temp), str(sta1.params['associatedTo'][0].name)))
			f_sta1_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta1.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta1.params['associatedTo'][0].name, sta1.get_distance_to(sta1.params['associatedTo'][0])) )
			
		#f_sta1_data.write('{"time":"%s", "sta":"%s", "distanceToRef":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta1.name), sta1.get_distance_to(sta1.params['associatedTo'][0]), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta1.params['associatedTo'][0].name) )
		#f_sta1_data.write('{"time":"%s", "sta":"%s", "x":"%s", "y": "%s", "z":"%s", "ref":"%s", "distanceToRef":"%s"}\n' %(str(int(round(time.time() * 1000))),str(sta1.name), line[1].split(",")[0], line[1].split(",")[1], line[1].split(",")[2],sta1.params['associatedTo'][0].name, sta1.get_distance_to(sta1.params['associatedTo'][0])) )
		"""
		f_sta1_data.write( '[' + str(int(round(time.time() * 1000))) + ",")
		f_sta1_data.write(str(line[0]) + ",")
		f_sta1.write(str(sta1.params['apsInRange']) + ",")
		f_sta1.write(str(sta1.params['associatedTo']) + ",")
		f_sta1.write(str(sta1.params['rssi']) + ",")
		f_sta1.write(str(sta1.params['position']) + ",")
		f_sta1.write(str(sta1.params['mac']) + "]\n")
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
		
		#time.sleep(0.05)
	
	f_sta1.close()
	f_sta1_data.close()
	f_ap1.close()
	f_ap2.close()
	f_ap3.close()
	f_ap4.close()
	f_ml.close()
	
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

