#!/usr/bin/python

#Replaying Mobility
"""Se crea un hilo para realizar movimiento independiente de las estaciones
 (Se descubre que al crear el hilo la grafica no se actualiza (ya que la grafica esta en el hilo principal))"""


from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.replaying import replayingMobility
from mn_wifi.node import OVSAP
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.wmediumdConnector import interference
import os
import time
import threading

def topology():
	"Create a network."
	net = Mininet_wifi(controller=Controller, accessPoint=OVSAP,
					   link=wmediumd, wmediumd_mode=interference)

	info("*** Creating nodes\n")
	sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8', position='30,50,0')
	sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8', position='55,50,0')
	#sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.3/8', speed=3)
	#sta4 = net.addStation('sta4', mac='00:00:00:00:00:05', ip='10.0.0.4/8', speed=3)

	ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1', position='45,45,0')

	c1 = net.addController('c1', controller=Controller)

	info("*** Configuring Propagation Model\n")
	net.setPropagationModel(model="logDistance", exp=4.5)

	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	#path = os.path.dirname(os.path.abspath(__file__))
	
	#getTrace(sta2, 'pox1.txt')
	#getTrace(sta3, '%s/replayingMobility/node3.dat' % path, net)
	#getTrace(sta4, '%s/replayingMobility/node4.dat' % path, net)
	
	'ploting graph'
	#net.plotGraph(max_x=100, max_y=100)
	
	#positionDevice(sta1, 'pox1.txt')
	
	
	info("*** Starting network\n")
	net.start()
	#net.build()
	#c1.start()
	#ap1.start([c1])
	
	hilo = threading.Thread(name='positionDevice', target=positionDevice, args=(sta1,'pox1.txt', net))
	#hilo.daemon = True
	hilo.start()
	#replayingMobility(net)

	info("*** Running CLI\n")
	CLI_wifi(net)
	

	
	"""print('Cambio posicion 1')
	sta1.setPosition('30,50,0')
	time.sleep(.400)
	print('Cambio posicion 1')
	sta1.setPosition('60,50,0')
	time.sleep(.400)
	print('Cambio posicion 1')
	sta1.setPosition('80,50,0')"""

	info("*** Stopping network\n")
	net.stop()

def positionDevice(sta,file_, net):
	
	#net.plotGraph(max_x=100, max_y=100)
	time.sleep(.800)
	print('Cambio posicion 1')
	sta.setPosition('50,80,0')
	time.sleep(.800)
	print('Cambio posicion 2')
	sta.setPosition('60,50,0')
	time.sleep(.800)
	print('Cambio posicion 3')
	sta.setPosition('80,50,0')
	
	file_ = open(file_, 'r')
	raw_data = file_.readlines()
	file_.close()
	
	for data in raw_data:
		line = data.split()
		print('Cambio posicion')
		sta.setPosition(line[1])
		print(sta.params['position'])
		time.sleep(.200)

def getTrace(sta, file_):

	#net.isReplaying = True

	file_ = open(file_, 'r')
	raw_data = file_.readlines()
	file_.close()

	sta.position = []

	for data in raw_data:
		line = data.split()
		sta.position.append(line[1])
		#x = line[0]  # First Column
		#y = line[1]  # Second Column
		sta.position.append('%s,%s,0' % (x, y))
		
if __name__ == '__main__':
	setLogLevel('info')
	topology()
