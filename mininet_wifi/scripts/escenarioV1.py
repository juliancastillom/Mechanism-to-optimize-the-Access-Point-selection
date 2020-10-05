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
	u1_d1 = net.addStation('u1_d1', ip='10.0.0.1', position='10.0,200.0,0', range = 20)
	u1_d2 = net.addStation('u1_d2', ip='10.0.0.2', position='10.0,200.0,0', range = 20)
	u1_d3 = net.addStation('u1_d3', ip='10.0.0.3', position='10.0,200.0,0', range = 20)
	
	u2_d1 = net.addStation('u2_d1', ip='10.0.0.4', position='170.0,100.0,0', range = 20)
	u2_d2 = net.addStation('u2_d2', ip='10.0.0.5', position='170.0,100.0,0', range = 20)
	u2_d3 = net.addStation('u2_d3', ip='10.0.0.6', position='170.0,100.0,0', range = 20)
	u2_d4 = net.addStation('u2_d4', ip='10.0.0.7', position='170.0,100.0,0', range = 20)
	
	#AP4
	sta1 = net.addStation('sta1', ip='10.0.0.8',min_x=60,max_x=140, min_y=50, max_y=160, min_v=20, max_v=30, position='90.0,130.0,0', range = 20)
	#sta1 = net.addStation('sta1', ip='10.0.0.8',min_x=60,max_x=140, min_y=50, max_y=160, min_v=20, max_v=30, range = 20)
	#sta1 = net.addStation('sta1', ip='10.0.0.8', range = 20)
	sta6 = net.addStation('sta6', ip='10.0.0.13', position='125.8,180.0,0', range = 20)
	sta7 = net.addStation('sta7', ip='10.0.0.14', position='150.0,50.0,0', range = 20)
	sta8 = net.addStation('sta8', ip='10.0.0.15', position='74.0,162.0,0', range = 20)
	sta9 = net.addStation('sta9', ip='10.0.0.16', position='75.0,75.0,0', range = 20)
	sta10 = net.addStation('sta10', ip='10.0.0.17', position='117.0,173.0,0', range = 20)
	
	#AP3
	sta4 = net.addStation('sta4', ip='10.0.0.11', position='170.0,213.0,0', range = 20)
	sta5 = net.addStation('sta5', ip='10.0.0.12', position='180.0,213.0,0', range = 20)
	
	#AP2
	sta2 = net.addStation('sta2', ip='10.0.0.9', position='120.0,225.0,0', range = 20)
	#sta2 = net.addStation('sta2', ip='10.0.0.9', range = 20)
	sta3 = net.addStation('sta3', ip='10.0.0.10', position='80.0,240.0,0', range = 20)
	
	h1 = net.addHost( 'h1', ip='10.0.0.13', mac='00:00:00:00:00:13' )

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
	
	"""net.addLink(ap1, sta1)
	net.addLink(ap1, sta2)
	net.addLink(ap1, sta3)
	net.addLink(ap1, sta4)
	net.addLink(ap1, sta5)
	
	net.addLink(ap2, sta1)
	net.addLink(ap2, sta2)
	net.addLink(ap2, sta3)
	net.addLink(ap2, sta4)
	net.addLink(ap2, sta5)"""

	net.plotGraph(max_x=250, max_y=280)
	
	
	u1_start = '10.0,200.0,0'
	u1_stop = '200.0,210.0,0'
	
	u2_start = '170.0,100.0,0'
	u2_stop = '117.0,200.0,0'
	
	
	#net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100,min_v=0.1, max_v=0.2, seed=20)
	
	
	net.startMobility( time=0, repetitions=3, AC='ssf')
	
	net.mobility( u1_d1, 'start', time=1, position= u1_start)
	net.mobility( u1_d1, 'stop', time=29, position= u1_stop)
	
	net.mobility( u1_d2, 'start', time=1, position= u1_start)
	net.mobility( u1_d2, 'stop', time=29, position= u1_stop)
	
	net.mobility( u1_d3, 'start', time=1, position= u1_start)
	net.mobility( u1_d3, 'stop', time=29, position= u1_stop)
	
	net.mobility( u2_d1, 'start', time=3, position= u2_start)
	net.mobility( u2_d1, 'stop', time=29, position= u2_stop)
	
	net.mobility( u2_d2, 'start', time=3, position= u2_start)
	net.mobility( u2_d2, 'stop', time=29, position= u2_stop)
	
	net.mobility( u2_d3, 'start', time=3, position= u2_start)
	net.mobility( u2_d3, 'stop', time=29, position= u2_stop)
	
	net.mobility( u2_d4, 'start', time=3, position= u2_start)
	net.mobility( u2_d4, 'stop', time=29, position= u2_stop)
	
	#net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, seed=20)
	
	net.stopMobility( time=30 )
	
	
	"""if coord:
		sta1.coord = ['95.0,130.0,0', '180.0,230.0,0', '140.0,130.0,0']
		sta2.coord = ['125.0,225.0,0', '145.0,225.0,0', '160.0,250.0,0']

	net.startMobility(time=0, repetitions=2)
	if coord:
		net.mobility(sta1, 'start', time=1)
		net.mobility(sta2, 'start', time=2)
		net.mobility(sta1, 'stop', time=12)
		net.mobility(sta2, 'stop', time=22)
	else:
		net.mobility(sta1, 'start', time=1, position='95.0,130.0,0')
		net.mobility(sta2, 'start', time=2, position='125.0,225.0,0')
		net.mobility(sta1, 'stop', time=12, position='140.0,130.0,0')
		net.mobility(sta2, 'stop', time=22, position='145.0,225.0,0')
	net.stopMobility(time=23)"""
	
	info( '*** Starting network\n')
	net.build()
	net.start()
	"""info( '*** Starting controllers\n')
	for controller in net.controllers:
		controller.start()

	info( '*** Starting switches/APs\n')
	net.get('ap1').start([])
	net.get('ap2').start([])
	net.get('s1').start([c0])"""
	
	
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

