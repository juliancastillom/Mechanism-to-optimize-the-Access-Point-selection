#!/usr/bin/python

from mininet.node import Controller, OVSKernelSwitch
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


def myNetwork():
	#coord = True if '-c' in sys.argv else False

	net = Mininet_wifi( topo=None, build=False, link=wmediumd, wmediumd_mode=interference, ipBase='10.0.0.0/8')

	info( '*** Adding controller\n' )
	c0=net.addController(name='c0', controller=Controller, protocol='tcp', port=6633)

	info( '*** Add switches/APs\n')
	ap1 = net.addAccessPoint('ap1', cls=OVSKernelAP, ssid='ap1-ssid', channel='1', mode='g', position='20.0,200.0,0', range = 20)
	ap2 = net.addAccessPoint('ap2', cls=OVSKernelAP, ssid='ap2-ssid', channel='1', mode='g', position='80.0,200.0,0', range = 50)
	ap3 = net.addAccessPoint('ap3', cls=OVSKernelAP, ssid='ap3-ssid', mode='g', channel='7', position='155.0,200.0,0', range=50)
	ap4 = net.addAccessPoint('ap4', cls=OVSKernelAP, ssid='ap4-ssid', mode='g', channel='11', position='117.5,100.0,0', range=100)
	s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

	info( '*** Add hosts/stations\n')
	
	""" 
	--------------------------------------------------------------------
	-------------------------- Info Devices ----------------------------
	
								**** MAC **** 							
	00.00.00.00.xx.00 --> xx = user_number ()
	00.00.00.00.00.xx --> xx = device_number
	xx.00.00.00.00.00 --> xx = device_id
	
	example--> 01.00.00.00.02.03 --> devide_id(01) = smartphone, user_number(02) = user number 2, device_number(03) = device number 3
	
	
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
	
	u1_d1 = net.addStation('u1_d1', ip='10.0.0.1', mac='00:00:00:00:01:01', position='10.0,200.0,0', range = 20, speed = 1)
	u1_d2 = net.addStation('u1_d2', ip='10.0.0.2', mac='00:00:00:00:01:02', position='10.0,200.0,0', range = 20, speed = 1)
	u1_d3 = net.addStation('u1_d3', ip='10.0.0.3', mac='00:00:00:00:01:03', position='10.0,200.0,0', range = 20, speed = 1)
	
	u2_d1 = net.addStation('u2_d1', ip='10.0.0.4', mac='00:00:00:00:02:01', position='170.0,100.0,0', range = 20, speed = 2)
	u2_d2 = net.addStation('u2_d2', ip='10.0.0.5', mac='00:00:00:00:02:02', position='170.0,100.0,0', range = 20, speed = 2)
	u2_d3 = net.addStation('u2_d3', ip='10.0.0.6', mac='00:00:00:00:02:03', position='170.0,100.0,0', range = 20, speed = 2)
	u2_d4 = net.addStation('u2_d4', ip='10.0.0.7', mac='00:00:00:00:02:04', position='170.0,100.0,0', range = 20, speed = 2)
	
	#AP4
	sta1 = net.addStation('sta1', ip='10.0.0.8', mac='00:00:00:00:09:01', position='90.0,130.0,0', range = 20)
	sta6 = net.addStation('sta6', ip='10.0.0.13', mac='00:00:00:00:09:06', position='125.8,180.0,0', range = 20)
	sta7 = net.addStation('sta7', ip='10.0.0.14', mac='00:00:00:00:09:07', position='150.0,50.0,0', range = 20)
	sta8 = net.addStation('sta8', ip='10.0.0.15', mac='00:00:00:00:09:08', position='74.0,162.0,0', range = 20)
	sta9 = net.addStation('sta9', ip='10.0.0.16', mac='00:00:00:00:09:09', position='75.0,75.0,0', range = 20)
	sta10 = net.addStation('sta10', ip='10.0.0.17', mac='00:00:00:00:09:10', position='117.0,173.0,0', range = 20)
	
	#AP3
	sta4 = net.addStation('sta4', ip='10.0.0.11', mac='00:00:00:00:09:04', position='170.0,213.0,0', range = 20)
	sta5 = net.addStation('sta5', ip='10.0.0.12', mac='00:00:00:00:09:05', position='180.0,213.0,0', range = 20)
	
	#AP2
	sta2 = net.addStation('sta2', ip='10.0.0.9', mac='00:00:00:00:09:02', position='120.0,225.0,0', range = 20)
	#sta2 = net.addStation('sta2', ip='10.0.0.9', range = 20)
	sta3 = net.addStation('sta3', ip='10.0.0.10', mac='00:00:00:00:09:03', position='80.0,240.0,0', range = 20)
	
	h1 = net.addHost( 'h1', ip='10.0.0.13', mac='00:00:00:00:10:01' )

	info("*** Configuring Propagation Model\n")
	net.setPropagationModel(model="logDistance", exp=3)

	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	#net.setChannelEquation(bw='5', loss='0.04', delay='0', latency='0')

	info( '*** Add links\n')

	net.addLink(s1, ap1)
	net.addLink(s1, ap2)
	net.addLink(s1, ap3)
	net.addLink(s1, ap4)
	
	net.addLink(ap1, ap2)
	net.addLink(ap2, ap3)
	net.addLink(ap2, ap4)
	
	net.addLink(s1, h1)
	
	#net.plotGraph(max_x=250, max_y=280)
	
	#Asignar el recorrido del dispositivo
	getTrace(u1_d1, 'u1_mov.txt')
	getTrace(u1_d2, 'u1_mov.txt')
	getTrace(u1_d3, 'u1_mov.txt')
	
	getTrace(u2_d1, 'u2_mov.txt')
	getTrace(u2_d2, 'u2_mov.txt')
	getTrace(u2_d3, 'u2_mov.txt')
	getTrace(u2_d4, 'u2_mov.txt')
	
	
	info( '*** Starting network\n')
	net.build()
	net.start()
	

	#-------------------------------------------------------------------
	#-------------------Start IPERF and BW------------------------------
	#-------------------------------------------------------------------
	
	#------------------Iperf before configure BW------------------------
	print('\n---- Iperf before configure BW ----\n')
	#iperfTest()
	
	#------------------BW Configurarion---------------------------------
	print('\n---- IoT Device 1 ---- \n  ~~~~ Command to limit bandwidth ~~~~\n    .... wondershaper sta1-wlan0 2048 1024 ....')
	print sta1.cmd('wondershaper sta1-wlan0 2048 1024')
	
	
	print('\n---- IoT device 2 ---- \n  ~~~~ Command to limit bandwidth ~~~~\n    .... wondershaper sta2-wlan0 1024 512 ....')
	print sta2.cmd('wondershaper sta2-wlan0 1024 512')
	
	
	replayingMobility(net)
	
	
	#------------------Iperf after configure BW-------------------------
	
	print('---- Iperf after configure BW ----\n')
	#net.iperf((sta1, h1))
	#net.iperf((h1, sta1))
	
	
	#-------------------------------------------------------------------
	#-------------------End IPERF and BW--------------------------------
	#-------------------------------------------------------------------
	
	
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

