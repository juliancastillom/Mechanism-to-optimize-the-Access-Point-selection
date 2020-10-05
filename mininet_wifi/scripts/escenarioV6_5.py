#!/usr/bin/python
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
	
	f_handover = open("/home/mininet/Escritorio/scripts/output/f_hanfover.txt","w+")
	f_handover.close()

	info( '*** Add switches/APs\n')
	ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1', position='50.0,150.0,0', range = 45)
	ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='7', position='90.0,150.0,0', range = 30)
	ap3 = net.addAccessPoint('ap3', ssid='ap3-ssid', mode='g', channel='11', position='130.0,150.0,0', range=45)
	ap4 = net.addAccessPoint('ap4', ssid='ap4-ssid', mode='g', channel='11', position='50.0,90.0,0', range=40)
	s1 = net.addSwitch('s1')

	info( '*** Add hosts/stations\n')
	
	""" 
	--------------------------------------------------------------------
	-------------------------- Info Devices ----------------------------
	
								**** MAC **** 							
	xx.00.00.00.00.00 --> xx = device_id
	00.xx.00.00.00.00 --> xx = user_number
	00.00.xx.00.00.00 --> xx = device_number
	
	
	example--> 01.02.03.00.00.00 --> devide_id(01) = smartphone, user_number(02) = user number 2, device_number(03) = device number 3
	
	
							**** Device ids ****						
	01.xx.xx.xx.xx.xx = smartphone
	02.xx.xx.xx.xx.xx = smartband
	03.xx.xx.xx.xx.xx = smartwatch
	04.xx.xx.xx.xx.xx = sensor
	05.xx.xx.xx.xx.xx = sensor
	06.xx.xx.xx.xx.xx = sensor
	07.xx.xx.xx.xx.xx = sensor
	--------------------------------------------------------------------
	--------------------------------------------------------------------
	
	
	--------------------------------------------------------------------
	----------------------------- Names --------------------------------
	
	uX_dX --> uX = user number n, dX = device number n. n = (0-inf)
	
	--------------------------------------------------------------------
	--------------------------------------------------------------------
	
	
	--------------------------------------------------------------------
	------------------------ Movement files ----------------------------
	
	uX_mov --> uX = user number n - movements
	
	staX_mov --> staX = sta number n - movements
	
	--------------------------------------------------------------------
	--------------------------------------------------------------------
	"""
	
	u1_d1 = net.addStation('u1_d1', ip='10.0.0.134', mac='01:01:01:00:01:01', position='10.0,150.0,0', range = 20, speed = 1, otherParam = 3, battery = 100)
	u1_d2 = net.addStation('u1_d2', ip='10.0.0.2', mac='02:01:02:00:01:02', position='10.0,150.0,0', range = 20, speed = 1)
	u1_d3 = net.addStation('u1_d3', ip='10.0.0.3', mac='03:01:03:00:01:03', position='10.0,150.0,0', range = 20, speed = 1)
	
	u2_d1 = net.addStation('u2_d1', ip='10.0.0.4', mac='01:02:01:00:02:01', position='25.0,70.0,0', range = 20, speed = 2)
	u2_d2 = net.addStation('u2_d2', ip='10.0.0.5', mac='02:02:02:00:02:02', position='25.0,70.0,0', range = 20, speed = 2)
	u2_d3 = net.addStation('u2_d3', ip='10.0.0.6', mac='03:02:03:00:02:03', position='25.0,70.0,0', range = 20, speed = 2)
	u2_d4 = net.addStation('u2_d4', ip='10.0.0.7', mac='04:02:04:00:02:04', position='25.0,70.0,0', range = 20, speed = 2)
	
	#AP2
	sta1 = net.addStation('sta1', ip='10.0.1.123', mac='00:00:00:00:09:01', position='90.0,120.0,0', range = 20, speed = 5)
	sta8 = net.addStation('sta8', ip='10.0.1.8', mac='00:00:00:00:09:08', position='91.0,175.0,0', range = 20)
	
	#AP4
	sta9 = net.addStation('sta9', ip='10.0.1.9', mac='00:00:00:00:09:09', position='75.0,75.0,0', range = 20)
	sta10 = net.addStation('sta10', ip='10.0.1.10', mac='00:00:00:00:09:10', position='35.0,95.0,0', range = 20)
	
	#AP3
	sta4 = net.addStation('sta4', ip='10.0.1.4', mac='00:00:00:00:09:04', position='125.0,110.0,0', range = 20)
	sta5 = net.addStation('sta5', ip='10.0.1.5', mac='00:00:00:00:09:05', position='160.0,125.0,0', range = 20)
	sta6 = net.addStation('sta6', ip='10.0.1.6', mac='00:00:00:00:09:06', position='125.0,180.0,0', range = 20)
	sta7 = net.addStation('sta7', ip='10.0.1.7', mac='00:00:00:00:09:07', position='110.0,170.0,0', range = 20)
	
	#AP1
	sta2 = net.addStation('sta2', ip='10.0.1.2', mac='00:00:00:00:09:02', position='30.0,180.0,0', range = 20)
	#sta2 = net.addStation('sta2', ip='10.0.0.9', range = 20)
	sta3 = net.addStation('sta3', ip='10.0.1.3', mac='00:00:00:00:09:03', position='50.0,125.0,0', range = 20)
	
	h1 = net.addHost( 'h1', ip='10.0.2.123', mac='00:00:00:00:10:01' )

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
	#net.setAssociationCtrl( 'slf' )  
	net.setAssociationCtrl( 'slf2' )
	
	
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
	
	#getTrace(sta1, 'u3_mov.txt')   #Uncomment >> replayingMobility(net)
	
	info( '*** Starting network\n')
	net.build()
	net.start()
	
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
	print sta2.cmd('touch sta_output/sta2_file.txt') #Crear archivo automaticamente
	#print sta2.cmd('python aleat.py')
	#print sta2.cmd('python aleat.py &')
	
	
	#--------------------VIDEO APPLICATION------------------------------
	print ('Server VLC')
	print sta3.cmd("sh serverVlc.sh &")
	time.sleep(1)
	
	print ('Client VLC')
	print sta4.cmd("sh clientVlc.sh &")
	time.sleep(1)
	
	#---------------------DATA APPLICATION------------------------------
	print ('Server Socket')
	#print sta5.cmd("python serverSocket.py &")
	sta5.cmd("python serverSocket.py &")
	
	print ('Client Socket')
	#print sta6.cmd("python clientSocket.py &")
	sta6.cmd("python clientSocket.py &")
	
	#replayingMobility(net)
	
	#------------------Iperf after configure BW-------------------------
	
	print('---- Iperf after configure BW ----\n')
	#net.iperf((sta1, h1))
	#net.iperf((h1, sta1))
	
	#Movimiento de una estacion de acuerdo a un txt con las coordenadas
	file_mov = "u4_mov.txt"
	mov1 = open(file_mov, 'r')
	raw_data = mov1.readlines()
	mov1.close()
	f_sta1= open("output/sta1_params.txt","w+")
	f_ap1= open("output/ap1_params.txt","w+")
	f_ap2= open("output/ap2_params.txt","w+")
	f_ap3= open("output/ap3_params.txt","w+")
	f_ap4= open("output/ap4_params.txt","w+")
	
	for data in raw_data:
		line = data.split()
		sta1.setPosition("{}".format(line[1]))
		#print('Time mov ' + time.strftime("%H:%M:%S") )
		#print('Time mov milliseconds' + str(int(round(time.time() * 1000))) )
		#print('Time mov milliseconds 2 ' + str(time.time()) )
		"""
		print ("********************************************************")
		print("Mov # " + str(line[0]))
		print ("Position: " + str(sta1.params['position']))
		print ("-----------------------")
		print ("AP1: " + str(ap1.params['stationsInRange']))
		print ("-----------------------")
		print ("AP2: " + str(ap2.params['stationsInRange']))
		print ("-----------------------")
		print ("AP3: " + str(ap3.params['stationsInRange']))
		print ("-----------------------")
		print ("RSSI Sta1: " + str(sta1.params['rssi']))
		print ("-----------------------")
		print ("Associated to: " + str(sta1.params['associatedTo']))
		"""
		f_sta1.write( '[' + str(int(round(time.time() * 1000))) + ",")
		f_sta1.write(str(line[0]) + ",")
		f_sta1.write(str(sta1.params['apsInRange']) + ",")
		f_sta1.write(str(sta1.params['associatedTo']) + ",")
		f_sta1.write(str(sta1.params['rssi']) + ",")
		f_sta1.write(str(sta1.params['position']) + ",")
		f_sta1.write(str(sta1.params['mac']) + "]\n\n")
		
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
	f_ap1.close()
	f_ap2.close()
	f_ap3.close()
	f_ap4.close()
	
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

