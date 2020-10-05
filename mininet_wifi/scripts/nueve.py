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

def myNetwork():

	net = Mininet_wifi( topo=None, build=False, link=wmediumd, wmediumd_mode=interference, ipBase='10.0.0.0/8')

	info( '*** Adding controller\n' )
	c0=net.addController(name='c0', controller=Controller, protocol='tcp', port=6633)

	info( '*** Add switches/APs\n')
	ap1 = net.addAccessPoint('ap1', cls=OVSKernelAP, ssid='ap1-ssid', channel='1', mode='g', position='80.0,80.0,0', range = 50)
	ap2 = net.addAccessPoint('ap2', cls=OVSKernelAP, ssid='ap2-ssid', channel='1', mode='g', position='200.0,80.0,0', range = 50)
	s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

	info( '*** Add hosts/stations\n')
	sta1 = net.addStation('sta1', ip='10.0.0.1', position='90.0,80.0,0', range = 20)
	sta2 = net.addStation('sta2', ip='10.0.0.2', position='110.0,80.0,0', range = 20)
	sta3 = net.addStation('sta3', ip='10.0.0.3', position='60.0,80.0,0', range = 20)
	sta4 = net.addStation('sta4', ip='10.0.0.4', position='40.0,80.0,0', range = 20)
	sta5 = net.addStation('sta5', ip='10.0.0.5', position='160.0,80.0,0', range = 20)
	h1 = net.addHost( 'h1', ip='10.0.0.6', mac='00:00:00:00:00:6' )

	info("*** Configuring Propagation Model\n")
	net.setPropagationModel(model="logDistance", exp=3)

	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	#net.setChannelEquation(bw='5', loss='0.04', delay='0', latency='0')

	info( '*** Add links\n')

	net.addLink(s1, ap1)
	net.addLink(s1, ap2)
	net.addLink(ap1, ap2)
	net.addLink(s1, h1)
	
	net.addLink(ap1, sta1)
	net.addLink(ap1, sta2)
	net.addLink(ap1, sta3)
	net.addLink(ap1, sta4)
	net.addLink(ap1, sta5)
	
	net.addLink(ap2, sta1)
	net.addLink(ap2, sta2)
	net.addLink(ap2, sta3)
	net.addLink(ap2, sta4)
	net.addLink(ap2, sta5)

	net.plotGraph(max_x=250, max_y=200)

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
	"""print('\n---- Iperf before configure BW ----\n')
	net.iperf((sta1, sta2))
	net.iperf((sta1, sta3))
	net.iperf((sta1, sta4))
	net.iperf((sta2, sta1))
	net.iperf((sta2, sta3))
	net.iperf((sta2, sta4))
	net.iperf((sta1, h1))
	net.iperf((h1, sta2))
	net.iperf((h1, sta3))
	net.iperf((h1, sta4))
	net.iperf((sta3, sta4))"""
	
	
	#------------------BW Configurarion---------------------------------
	print('\n---- IoT Device 1 ---- \n  ~~~~ Command to limit bandwidth ~~~~\n    .... tc qdisc add dev sta1-wlan0 root tbf rate 1024kbit latency 50ms burst 1540 ....')
	print sta1.cmd('tc qdisc add dev sta1-wlan0 root tbf rate 1024kbit latency 50ms burst 1540')
	
	
	print('\n---- IoT device 2 ---- \n  ~~~~ Command to limit bandwidth ~~~~\n    .... tc qdisc add dev sta2-wlan0 root tbf rate 2048kbit latency 100ms burst 1540 ....')
	print sta2.cmd('tc qdisc add dev sta2-wlan0 root tbf rate 2048kbit latency 100ms burst 1540')
	
	#------------------Iperf after configure BW-------------------------
	print('---- Iperf after configure BW ----\n')
	
	net.iperf((sta1, h1))
	net.iperf((h1, sta1))
	
	"""net.iperf((sta1, sta2))
	net.iperf((sta1, sta3))
	net.iperf((sta1, sta4))
	net.iperf((sta2, sta1))
	net.iperf((sta2, sta3))
	net.iperf((sta2, sta4))
	net.iperf((sta1, h1))
	net.iperf((h1, sta1))
	net.iperf((h1, sta2))
	net.iperf((h1, sta3))
	net.iperf((h1, sta4))
	net.iperf((sta3, sta4))"""
	#-------------------------------------------------------------------
	#-------------------End IPERF and BW--------------------------------
	#-------------------------------------------------------------------
	
	
	info( '*** Post configure nodes\n')
	CLI_wifi(net)
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	myNetwork()

