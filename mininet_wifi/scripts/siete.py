#!/usr/bin/python

'Setting the position of Nodes and providing mobility using mobility models'

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi


def topology():
	"Create a network."
	net = Mininet_wifi()

	info("*** Creating nodes\n")
	net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8', min_x=50, max_x=100, min_y=100, max_y=101, min_v=40, max_v=50, range = 20, position='70,80,0')
	net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8', min_x=60, max_x=70, min_y=10, max_y=20, min_v=1, max_v=5, range = 20, position='130,130,0')
	#ap1 = net.addAccessPoint('ap1', ssid='1-ssid', mode='g', channel='1', failMode="standalone", position='50,80,0', range = 40)
	ap1 = net.addAccessPoint('ap1', ssid='1-ssid', mode='g', channel='1', failMode="standalone", position='20,20,0', range = 10)
	#ap2 = net.addAccessPoint('ap2', ssid='2-ssid', mode='g', channel='1', failMode="standalone", position='90,80,0', range = 40)
	ap2 = net.addAccessPoint('ap2', ssid='2-ssid', mode='g', channel='1', failMode="standalone", position='90,80,0', range = 40)

	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	net.plotGraph(max_x=150, max_y=150)

	net.setMobilityModel(time=0, model='RandomDirection', max_x=130, max_y=130, seed=20)

	info("*** Starting network\n")
	net.build()
	ap1.start([])
	ap2.start([])

	info("*** Running CLI\n")
	CLI_wifi(net)

	info("*** Stopping network\n")
	net.stop()


if __name__ == '__main__':
	setLogLevel('info')
	topology()
