#!/usr/bin/python

'Example for Handover'

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
import threading


def topology():
	"Create a network."
	net = Mininet_wifi(controller=Controller)

	info("*** Creating nodes\n")
	#captura CapturaV1-1_test_handoverV2
	"""
	sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2',position='50,70,0', range=10)
	sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3',position='10,40,0', range=10)
	"""
	#captura CapturaV1-2_test_handoverV2
	sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2',position='50,70,0', range=10, active_scan=1, scan_freq="2412 2437 2462", freq_list="2412 2437 2462")
	sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3',position='10,40,0', range=10, active_scan=1, scan_freq="2412 2437 2462", freq_list="2412 2437 2462")
	
	ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='35,30,0', range=30)
	ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='6', position='75,30,0', range=30)
	ap3 = net.addAccessPoint('ap3', ssid='ssid-ap3', mode='g', channel='11', position='55,80,0', range=30)
	c1 = net.addController('c1')
	s1 = net.addSwitch('s1')

	#net.setPropagationModel(model="logDistance", exp=5)

	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	info("*** Creating links\n")
	#net.addLink(ap1, ap2)
	net.addLink(s1, ap1)
	net.addLink(s1, ap2)
	net.addLink(s1, ap3)

	net.plotGraph(max_x=120, max_y=120)
	net.setAssociationCtrl( 'ssf' )
	
	net.startMobility(time=3,repetitions=2)
	net.mobility(sta1, 'start', time=10, position='50,70,0')
	net.mobility(sta1, 'stop', time=25, position='60,30,0')
	net.stopMobility(time=25)
	
	info("*** Starting network\n")
	net.build()
	net.start()
	
	#hilo = threading.Thread(name='testPing', target=testPing, args=(sta1, sta2, net))
	#hilo.daemon = True
	#hilo.start()
	
	info("*** Running CLI\n")
	CLI_wifi(net)

	info("*** Stopping network\n")
	net.stop()

def testPing(sta1, sta2, net):
	print('inicio ping')
	print (sta1.cmd('ping -c100 %s' % sta2.IP()))
	print('Fin ping')
	#print (net.ping(sta1,sta2))

if __name__ == '__main__':
	setLogLevel('info')
	topology()
