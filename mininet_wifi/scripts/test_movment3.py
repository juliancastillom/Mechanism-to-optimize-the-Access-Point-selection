#!/usr/bin/python

'Replaying Mobility'

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.node import OVSAP
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.wmediumdConnector import interference
import os
from replay import replayingMobility
from replay import replayingMobility2


def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, accessPoint=OVSAP,
                       link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8', speed=4)
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8', speed=6)
    
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1', position='45,45,0')
    
    c1 = net.addController('c1', controller=Controller)

    info("*** Configuring Propagation Model\n")
    #net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")

    'ploting graph'
    #net.plotGraph(max_x=200, max_y=200)

    path = os.path.dirname(os.path.abspath(__file__))
    getTrace(sta1, 'pox1.txt')
    getTrace(sta2, 'pox2.txt')

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    
    #replayingMobility(net)
    #replayingMobility2(net)
    replayingMobility.addNode(sta1)
    replayingMobility(net)

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

def getTrace(sta, file_):

	file_ = open(file_, 'r')
	raw_data = file_.readlines()
	file_.close()
	sta.position = []
	for data in raw_data:
		line = data.split()
		#print('Cambio posicion')
		#sta.setPosition(line[1])
		sta.position.append(line[1])
		#print(sta.params['position'])
		#time.sleep(.200)
	


if __name__ == '__main__':
    setLogLevel('info')
    topology()
