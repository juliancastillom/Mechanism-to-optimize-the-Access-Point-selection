#!/usr/bin/python

'Setting mechanism to optimize the use of APs'

import sys
import os

from mininet.node import Controller #OVSKernelSwitch
from mininet.log import setLogLevel, info
from mn_wifi.node import UserAP, OVSKernelAP
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.replaying import replayingMobility
from mininet.term import cleanUpScreens, makeTerm
from time import sleep
import time
#from mn_wifi.link import wmediumd, adhoc
#from mn_wifi.wmediumdConnector import interference


#from mn_wifi.link import wmediumd
#from mn_wifi.wmediumdConnector import interference
#from subprocess import call
from mininet.link import TCLink
#import os
#from replay import replayingMobility
#from replay import replayingMobility2
#import time
from mn_wifi.associationControl import associationControl

def topology(isVirtual, acceso):
	"Create a network."
	net = Mininet_wifi(link=TCLink )
	net = Mininet_wifi(controller=Controller, accessPoint=UserAP)

	print ("acceso association control %s" %acceso)
	info("*** Creating nodes\n")
	#net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8')
	#net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8')
	#sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8' , active_scan=1, position='10.0,55.0,0',
	#			   min_x=20, max_x=100, min_y=55, max_y=55, min_v=5, max_v=10)
	#sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8', active_scan=1, position='110.0,35.0,0',
	#			   min_x=20, max_x=90, min_y=35, max_y=35, min_v=1, max_v=5)

	sta2 = net.addStation('sta2', ip='10.0.0.4/8', mac='00:00:00:00:00:03', position='140.0,160.0,0', range = 20)

	#sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8', min_x=40, max_x=140, min_y=20, max_y=160, min_v=30, max_v=50, min_wt=0, max_wt=10, battery = 100, speed=1)

	sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8', battery = 100)

	#sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8', min_x=40, max_x=90, min_y=30, max_y=35, min_v=5, max_v=8, min_wt=0, max_wt=20, battery = 100)
   
	#sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.4/8', min_x=10, max_x=90, min_y=30, max_y=35, min_v=1, max_v=2, min_wt=0, max_wt=10, battery = 100)

	#net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8')
	#net.addStation('sta4', mac='00:00:00:00:00:05', ip='10.0.0.5/8')
	#net.addStation('sta5', mac='00:00:00:00:00:06', ip='10.0.0.6/8')
	#net.addStation('sta6', mac='00:00:00:00:00:07', ip='10.0.0.7/8')
	#net.addStation('sta7', mac='00:00:00:00:00:08', ip='10.0.0.8/8')
	#net.addStation('sta8', mac='00:00:00:00:00:09', ip='10.0.0.9/8')
	#net.addStation('sta9', mac='00:00:00:00:00:10', ip='10.0.0.10/8')
	#net.addStation('sta10', mac='00:00:00:00:00:11', ip='10.0.0.11/8')

	ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='n', channel='1',
							 position='50,50,0', range=50, battery = 100)
	ap4 = net.addAccessPoint('ap4', ssid='ssid-ap4', mode='n', channel='11',
							 position='120,50,0', range=50, battery = 100)
	
	ap5 = net.addAccessPoint('ap5', ssid='ssid-ap5', mode='n', channel='1',
							 position='100,120,0', range=50, battery = 100)
	ap6 = net.addAccessPoint('ap6', ssid='ssid-ap6', mode='n', channel='6',
							 position='120,150,0', range=30, battery = 100)
	#if not isVirtual:
	print ("acceso association control %s" %acceso)
	ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='n', channel='6',
							 position='85,80,0', range=30, battery = 100)
	ap3 = net.addAccessPoint('ap3', ssid='ssid-ap3', mode='n', channel='8',
							 position='85,30,0', range=30, battery = 100)
	ap7 = net.addAccessPoint('ap7', ssid='ssid-ap7', mode='n', channel='11',
							 position='120,100,0', range=30, battery = 100)
	
	#if isVirtual:
	#	info("*** nvif CLI\n")
	#	sta1 = net.addStation('sta1', nvif=2)
	#else:
	#	sta1 = net.addStation('sta1')

	c1 = net.addController('c1', controller=Controller)
	#s1 = net.addSwitch('s1')
	#s1.listenPort=6634
	h1 = net.addHost('h1', ip='10.0.0.3/8')

	net.setPropagationModel(model="logDistance", exp=5)
	
	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()


	#net.plotNode(h1, position='35,90,0')
	#s1.plot(position='35,80,0')

	info("*** Associating and Creating links\n")
	"""net.addLink(ap1, s1)
	net.addLink(ap2, s1)
	net.addLink(ap3, s1)
	net.addLink(ap4, s1)
	net.addLink(ap5, s1)
	net.addLink(ap6, s1)
	net.addLink(ap7, s1) """

	net.addLink(ap1, ap2)
	net.addLink(ap2, ap3)
	net.addLink(ap3, ap4)
	net.addLink(ap4, ap5)
	net.addLink(ap5, ap6)
	net.addLink(ap6, ap7)
	

	net.addLink(h1, ap6)
	net.addLink(sta2, ap6)

	print "*** Enabling association control (AP)"
	net.setAssociationCtrl( 'topsis' )
	#net.setAssociationCtrl( 'llf' ) 

	#net.startMobility(time=0, model='RandomWayPoint', max_x=120, max_y=120,
	#				  min_v=0.3, max_v=0.5, seed=1, associationControl='ssf')

	#net.startMobility(time=0, model='RandomDirection', max_x=180, max_y=180,
	#					 min_v=0.5, max_v=0.8, seed=1, associationControl='ssf')

	#net.setMobilityModel(time=0, model='RandomWayPoint', max_x=180, max_y=180,
	#					 seed=20, ac_method='ssf')

	#net.setMobilityModel(time=0, model='GaussMarkov', max_x=180, max_y=180,
	#					 seed=20, ac_method='ssf')


# METODO DE MOVIMIENTO 1 - para mover un dispositivo de un punto a otro con el metodo net.startMobility
	u1_start = '60.0,10.0,0'
	u1_stop = '140.0,158.0,0'

	net.plotGraph(max_x=180, max_y=180)

	"""
	net.startMobility( time=5, repetitions=1, ac_method='ssf')
	net.mobility( sta1, 'start', time=5, position= u1_start)
	net.mobility( sta1, 'stop', time=65, position= u1_stop)
	net.stopMobility( time=75 )"""


	net.startMobility( time=5, repetitions=1, ac_method='topsis')
	net.mobility( sta1, 'start', time=5, position= u1_start)
	net.mobility( sta1, 'stop', time=35, position= u1_stop)
	net.stopMobility( time=45 )

	tiempoInit = time.time()
	print("tiempo inicial %s" %str(tiempoInit))
	print('tiempo inicial: ' + str(tiempoInit))
	#net.setMobilityModel(time=0, model='RandomWayPoint', max_x=100, max_y=100, seed=20)
	#print "*** Change mobility"
	#net.startMobility( time=40, repetitions=3, associationControl='ssf')
	#net.mobility( sta1, 'start', time=41, position= u1_stop)
	#net.mobility( sta1, 'stop', time=69, position= u1_start)
	
	#net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, seed=20)
	
	#net.stopMobility( time=70 )


	
	# METODO DE MOVIMIENTO 2 - El dispositivo toma las coordenadas de los archivos u1_mov.txt y u2_mov.txt
	# La velocidad del movimiento se configura en con el parametro 'speed' cuando se configuran los dispositivos
	#Cuando se use este metodo descomentar la linea 'replayingMobility2(net)'
	#getTrace(sta1, 'u5_mov.txt')
	
	#path = os.path.dirname(os.path.abspath(__file__))
	#print path
	#getTrace(sta1, '%s/u5_mov.txt' % path, net)

	#net.plotGraph(max_x=180, max_y=180)
	
	info("*** Starting network\n")
	net.build()
	c1.start()
	ap1.start([c1])
	ap2.start([c1])
	ap3.start([c1])
	ap4.start([c1])
	ap5.start([c1])
	ap6.start([c1])
	ap7.start([c1])
	#s1.start([c1])
	
	#replayingMobility(net)
	#os.system('xterm sta1 sta2')
#sta1.setRange(15)
#sta1.cmd('iwconfig sta1-wlan0 essid %s ap %s' % (ap1.params['ssid'][1], ap1.params['mac'][1]))
#ap1.cmd('dpctl unix:/tmp/ap1 meter-mod cmd=add,flags=1,meter=1 drop:rate=100')
#ap1.cmd('dpctl unix:/tmp/ap1 flow-mod table=0,cmd=add in_port=2 meter:1 apply:output=flood')
#ap1.cmd('dpctl unix:/tmp/ap1 flow-mod table=0,cmd=add in_port=3 meter:2 apply:output=flood')
#enb1.cmd('ovs-ofctl add-flow "enb1" in_port=1,udp,tp_src=8000,actions=controller')
#enb2.cmd('ovs-ofctl add-flow "enb2" in_port=1,udp,tp_src=8000,actions=controller')
	#s1.cmd('ovs-ofctl add-flow "s1" in_port=8,actions=output:7')
	#s1.cmd('ovs-ofctl add-flow "s1" in_port=7,actions=output:8')
	#net.dpctl('del-flows')

#os.system('ip link set hwsim0 up')
	#os.system('pkill -f \"xterm -title\"')
	#makeTerm( h1, cmd="bash -c 'iperf -s -i 1 -u;'" )
	#makeTerm( sta1, cmd="bash -c 'ping 10.0.0.4;'" )
	
	makeTerm( sta2, cmd="bash -c 'iperf -s -u -p 5566 -i 1 > resultiperf;'" )
	sleep(1)
	makeTerm( sta1, cmd="bash -c 'iperf -c 10.0.0.4 -u -b 2M -t 50 -p 5566;'" )

#ITGSend -T TCP  -a 10.0.0.4 -C 10 -c 100 -t 60000 -l sender21.log -x receiver12.log

	#makeTerm( sta2, cmd="bash -c 'ITGRecv -l receiverm1.log;'" )
	#sleep(1)
	"""makeTerm( sta1, cmd="bash -c 'ITGSend -T TCP  -a 10.0.0.4 -C 10 -c 100 -t 80000 -l sender21.log -x receiver12.log;'" )"""
	#makeTerm( sta1, cmd="bash -c 'ITGSend -T TCP  -a 10.0.0.4 -C 10 -c 100 -t 170000 -l sender21.log -x receiver12.log;'" )
	#makeTerm( sta1, cmd="bash -c 'ITGSend script_file1 -l senderm1.log;'" )

#	makeTerms( h3, cmd="bash -c 'iperf -s -i 1 -u;'" )
#	makeTerm( h4, cmd="bash -c 'iperf -s -i 1 -u;'" )

	#net.startTerms()
	#sleep(4)
	#sta2.sendcmd('ITGRecv \n')

	info("*** Running CLI\n")
	CLI_wifi(net)

	#os.system('pkill -f \"xterm -title\"')
	info("*** Stopping network\n")
	net.stop()
	#os.system('pkill -f \"xterm -title\"')

#def getTrace(sta, file_):

#	file_ = open(file_, 'r')
#	raw_data = file_.readlines()
#	file_.close()
#	sta.position = []
#	for data in raw_data:
#		line = data.split()
#		sta.position.append(line[1])


def getTrace(sta, file_, net):

	net.isReplaying = True
	file_ = open(file_, 'r')
	raw_data = file_.readlines()
	file_.close()

	sta.position = []
	pos = '-1000,0,0'
	sta.params['position'] = [float(x) for x in pos.split(',')]

	for data in raw_data:
		line = data.split()
		#print line
		x = line[1]  # First Column
		y = line[2]  # Second Column
		pos = float(x),float(y),0.0
		#pos = line[1]
		sta.position.append(pos)

if __name__ == '__main__':
	setLogLevel('info')
	isVirtual = True if '-v' in sys.argv else False
	acceso = "rssi" if '-r' in sys.argv else "onto"
	topology(isVirtual, acceso)
