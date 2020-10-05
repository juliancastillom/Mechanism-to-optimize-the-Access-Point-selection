#!/usr/bin/python
#Escenario escogido 2

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
import threading


def myNetwork():
	#coord = True if '-c' in sys.argv else False

	#net = Mininet_wifi(controller=RemoteController, link=TCLink )
	net = Mininet_wifi(link=TCLink )

	info( '*** Adding controller\n' )
	#c0=net.addController(name='c0', controller=RemoteController, ip='10.0.2.15', port=6633 )
	c0=net.addController(name='c0', controller=Controller, protocol='tcp', port=6633)

	info( '*** Add switches/APs\n')
	ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1', position='50.0,150.0,0', range = 45)
	ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='1', position='90.0,150.0,0', range = 30)
	ap3 = net.addAccessPoint('ap3', ssid='ap3-ssid', mode='g', channel='1', position='130.0,150.0,0', range=45)
	ap4 = net.addAccessPoint('ap4', ssid='ap4-ssid', mode='g', channel='1', position='50.0,90.0,0', range=40)
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
	
	u1_d1 = net.addStation('u1_d1', ip='10.0.0.134', mac='01:01:01:00:01:01', position='10.0,150.0,0', range = 20, speed = 1)
	u1_d2 = net.addStation('u1_d2', ip='10.0.0.2', mac='02:01:02:00:01:02', position='10.0,150.0,0', range = 20, speed = 1)
	u1_d3 = net.addStation('u1_d3', ip='10.0.0.3', mac='03:01:03:00:01:03', position='10.0,150.0,0', range = 20, speed = 1)
	
	u2_d1 = net.addStation('u2_d1', ip='10.0.0.4', mac='01:02:01:00:02:01', position='25.0,70.0,0', range = 20, speed = 2)
	u2_d2 = net.addStation('u2_d2', ip='10.0.0.5', mac='02:02:02:00:02:02', position='25.0,70.0,0', range = 20, speed = 2)
	u2_d3 = net.addStation('u2_d3', ip='10.0.0.6', mac='03:02:03:00:02:03', position='25.0,70.0,0', range = 20, speed = 2)
	u2_d4 = net.addStation('u2_d4', ip='10.0.0.7', mac='04:02:04:00:02:04', position='25.0,70.0,0', range = 20, speed = 2)
	
	#AP2
	sta1 = net.addStation('sta1', ip='10.0.1.123', mac='00:00:00:00:09:01', position='50.0,150.0,0', range = 20, battery = 100)
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
	
	"""net.addLink(ap1, ap2)
	net.addLink(ap2, ap3)
	net.addLink(ap1, ap4)"""
	
	net.addLink(s1, h1)
	
	#net.addLink(s1,c0)
	"""net.addLink(ap1,c0)
	net.addLink(ap2,c0)
	net.addLink(ap3,c0)"""
	
	
	net.plotGraph(max_x=200, max_y=200)
	
	print "*** Enabling association control (AP)"
	#net.setAssociationCtrl( 'ssf' )
	#net.setAssociationCtrl( 'llf' )
	net.setAssociationCtrl( 'topsis' )
	
	"""
	u1_start = '10.0,150.0,0'
	u1_stop = '160.0,170.0,0'
	
	u2_start = '25.0,70.0,0'
	u2_stop = '90.0,150.0,0'
	
	
	net.startMobility( time=0, repetitions=3)
	
	net.mobility( u1_d1, 'start', time=1, position= u1_start)
	net.mobility( u1_d1, 'stop', time=29, position= u1_stop)
	
	net.mobility( u1_d2, 'start', time=1, position= u1_start)
	net.mobility( u1_d2, 'stop', time=29, position= u1_stop)
	
	net.mobility( u1_d3, 'start', time=1, position= u1_start)
	net.mobility( u1_d3, 'stop', time=29, position= u1_stop)
	
	#net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, seed=20)
	
	net.stopMobility( time=30 )
	"""
	
	#Asignar el recorrido del dispositivo
	"""getTrace(u1_d1, 'u1_mov.txt')
	getTrace(u1_d2, 'u1_mov.txt')
	getTrace(u1_d3, 'u1_mov.txt')
	
	getTrace(u2_d1, 'u2_mov.txt')
	getTrace(u2_d2, 'u2_mov.txt')
	getTrace(u2_d3, 'u2_mov.txt')
	getTrace(u2_d4, 'u2_mov.txt')
	"""
	
	"""
	sta1_start = '50.0,150.0,0'
	sta1_stop = '150.0,150.0,0'
	
	
	net.startMobility( time=0, repetitions=3)
	
	net.mobility( sta1, 'start', time=10, position= sta1_start)
	net.mobility( sta1, 'stop', time=100, position= sta1_stop)
	
	#net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, seed=20)
	
	net.stopMobility( time=100 )
	"""
	
	sta1_start = '50.0,150.0,0'
	sta1_stop = '150.0,150.0,0'
	
	
	net.startMobility( time=0, repetitions=1)
	
	net.mobility( sta1, 'start', time=1, position= sta1_start)
	net.mobility( sta1, 'stop', time=10, position= sta1_stop)
	
	#net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, seed=20)
	
	net.stopMobility( time=10 )
	
	info( '*** Starting network\n')
	net.build()
	net.start()
	"""c0.start()
	s1.start( [c0] )
	ap1.start( [c0] )
	ap2.start( [c0] )
	ap3.start( [c0] )
	ap4.start( [c0] )"""
	
	
	#prueba 1
	"""
	sta1.setRange(10)
	"""
	#prueba 2
	"""
	sta1.setRange(20)
	"""
	#prueba 3
	"""
	sta1.setRange(10)
	ap1.setRange(80)
	"""
	#prueba 4
	"""
	sta1.setRange(10)
	ap1.setRange(50)
	ap1.setAntennaGain(10, intf='ap1-wlan1')
	"""
	
	#prueba 5
	"""
	sta1.setRange(10)
	ap1.setRange(50)
	sta1.setAntennaGain(10, intf='sta1-wlan0')
	"""
	
	#prueba 6
	
	#sta1.setRange(10)
	#ap1.setRange(50)
	ap1.setTxPower(5, intf='ap1-wlan1')
	
	
	#prueba 7
	"""
	sta1.setRange(10)
	ap1.setRange(50)
	ap1.setTxPower(0.5, intf='ap1-wlan1')
	"""
	
	#prueba 8
	"""
	sta1.setRange(10)
	ap1.setRange(50)
	ap1.setTxPower(0.1, intf='ap1-wlan1')
	"""
	
	#prueba 9
	"""
	sta1.setRange(10)
	ap1.setRange(50)
	sta1.setTxPower(5, intf='sta1-wlan0')
	
	#prueba 9.1
	sta1.setRange(10)
	ap1.setRange(50)
	sta1.setTxPower(0.1, intf='sta1-wlan0')
	
	#prueba 9.2
	sta1.setRange(10)
	ap1.setRange(50)
	sta1.setTxPower(0.1, intf='sta1-wlan0')
	"""
	
	#prueba 10
	"""
	sta1.setRange(10)
	ap1.setRange(50)
	ap1.setAntennaGain(10, intf='ap1-wlan1')
	sta1.setAntennaGain(10, intf='sta1-wlan0')
	"""
	
	#prueba 11
	#sta1.setRange(10)
	#ap1.setRange(50)
	#ap1.setAntennaGain(10, intf='ap1-wlan1')
	#sta1.setAntennaGain(10, intf='sta1-wlan0')
	
	print('--------------------------------------------')
	print('PARAMETROS (tomados al inicio de la prueba)')
	print('-------------')
	
	print ("Sta1 PARAMS \n" + str(sta1.params))
	print ("AP1 PARAMS \n" + str(ap1.params))
	
	print('--------------------------------------------')
	print('INICIO PRUEBA')
	print('-------------')
	
	#net.ping("sta1", "sta2")
	#print sta1.cmd('ping -c100 %s' % sta2.IP())
	
	#hilo = threading.Thread(name='testPing', target=testPing, args=(sta1,sta2, str(time.strftime("%H:%M:%S") )))
	#hilo.daemon = True
	#hilo.start()
	
	"""print ('START sh ifconfig hwsim0 up')
	sta1.cmd('sh ifconfig hwsim0 up')
	time.sleep(2)
	print ('END sh ifconfig hwsim0 up')
	
	time.sleep(10)
	
	a = 0
	xs = 50.0
	ys = 150.0
	zs = 0.0
	print('inicio moivimiento' + time.strftime("%H:%M:%S") )
	while (a <= 100):
		print ("-----------------------------------------------------------------------------------------")
		print ("-----------------------------------------------------------------------------------------")
		print ("Numero " + str(a))
		posit = "{}, {}, {}".format(xs, ys, zs)
		#print(posit)
		sta1.setPosition("{}, {}, {}".format(xs, ys, zs))
		#print("py sta1.setPosition('{}, {}, {}')".format(x, a, a))
		#print("Sta1")
		#print("py sta1.setPosition('60.0, 150.0, 0.0')")
		print('inicio Ping' + time.strftime("%H:%M:%S") )
		print sta1.cmd('ping -c1 %s' % sta2.IP())
		print('Fin Ping' + time.strftime("%H:%M:%S") )
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
		#time.sleep(0.200)
		a = a + 1.0
		xs = xs + 1.0
	print ("END")
	print('fin moivimiento' + time.strftime("%H:%M:%S") )
	
	print('-----------')
	print('PARAMETROS (tomados al final de la prueba)')
	print('-------------')
	
	print ("Sta1 PARAMS \n" + str(sta1.params))
	print ("AP1 PARAMS \n" + str(ap1.params))
	
	print "*** Running CLI"
	"""
	#replayingMobility(net)
	
	info( '*** Post configure nodes\n')
	CLI_wifi(net)
	
	net.stop()

def testPing(sta1, sta2, time):
	
	print('inicio ping' + time)
	print sta1.cmd('ping -t1000 %s' % sta2.IP())
	print('fin ping' + time)
	
	#print ("Associated to: " + str(sta1.params['associatedTo']))

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

