#!/usr/bin/python

"""
Replaying Mobility Conditions
based in https://github.com/ramonfontes/reproducible-research/blob/master/mininet-wifi/The-Computer-Journal-2017/replayingNetwork/ieee80211b/replayingNetwork.py
"""

from mininet.cli import CLI
from mininet.link import TCLink
#from mininet.log import setLogLevel
#from mininet.net import Mininet
#from mn_wifi.net import Mininet_wifi
from mininet.node import Controller, OVSKernelSwitch
#from mn_wifi.replaying import replayingMobility

import os

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.replaying import replayingMobility
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.wmediumdConnector import interference


def topology():
	"Create a network."
	#net = Mininet_wifi(controller=Controller, link=TCLink, switch=OVSKernelSwitch)
	net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

	print "*** Creating nodes"
	sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', ip='192.168.0.1/24', speed = 2)
	sta2 = net.addStation('sta2', mac='00:00:00:00:00:02', ip='192.168.0.2/24', speed = 4)
	
	ap1 = net.addAccessPoint('ap1', range=20, ssid='ap1-ssid', mode='g', channel='1', position='50,50,0')
	
	c1 = net.addController('c1', controller=Controller)

	print "*** Configuring wifi nodes"
	net.configureWifiNodes()

	
	net.plotGraph(max_x=400, max_y=400)
	
	getTrace(sta1, 'pox1.txt', net)
	getTrace(sta2, 'pox2.txt', net)
	
	replayingMobility(net)
	
	#replayingMobility.addNode(sta1)
	#replayingMobility.addNode(sta2)
	
	
	print "*** Starting network"
	net.build()
	net.start()
	#c1.start()
	#ap1.start([c1])
	#sta1.cmd('iw dev sta1-wlan0 interface add mon0 type monitor &')
	#sta1.cmd('ifconfig mon0 up &')
	#sta2.cmd('iw dev sta2-wlan0 interface add mon0 type monitor &')
	#sta2.cmd('ifconfig mon0 up &')
	
	#net.autoAssociation()
	
	print "*** Running CLI"
	CLI(net)

	print "*** Stopping network"
	net.stop()


def getTrace(sta, file, net):
	net.isReplaying = True
	file = open(file, 'r')
	raw_data = file.readlines()
	file.close()

	sta.time = []
	sta.position = []
	pos = '-1000,0,0'
	sta.params['position'] = [float(x) for x in pos.split(',')]

	for data in raw_data:
		line = data.split()
		#sta.time.append(float(line[0]))  # First Column = Time
		sta.position.append(line[1]) # Second Column = Position x,y,z


if __name__ == '__main__':
	setLogLevel('debug')
	topology()
