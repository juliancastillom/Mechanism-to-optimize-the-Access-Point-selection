#!/usr/bin/python

'Replaying Mobility'
import os

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.replaying import replayingMobility
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.wmediumdConnector import interference
import time
from mininet.term import cleanUpScreens, makeTerm


def topology():
	"Create a network."
	net = Mininet_wifi(link=wmediumd,
					   wmediumd_mode=interference)
	c0=net.addController(name='c0', controller=Controller, protocol='tcp', port=6633)
	#asoc = "ssf"
	#asoc = "llf"
	#asoc = "llf2"
	#asoc = "slf"
	#asoc = "topsis"
	#asoc = "saw"
	asoc = "rf"
	#asoc = "dl"
	
	if asoc == "ssf":
		f_ssf= open("/home/mininet/Escritorio/scripts/output/ssf.txt","w+")
		f_ssf.close()
	elif asoc == "llf":
		f_llf= open("/home/mininet/Escritorio/scripts/output/llf.txt","w+")
		f_llf.close()
	elif asoc == "slf":
		f_slf= open("/home/mininet/Escritorio/scripts/output/slf.txt","w+")
		f_slf.close()
	elif asoc == "topsis":
		f_topsis= open("/home/mininet/Escritorio/scripts/output/topsis.txt","w+")
		f_topsis.close()
	elif asoc == "saw":
		f_topsis= open("/home/mininet/Escritorio/scripts/output/saw.txt","w+")
		f_topsis.close()
	elif asoc == "rf":
		f_rf= open("/home/mininet/Escritorio/scripts/output/rf.txt","w+")
		f_rf.close()
	elif asoc == "dl":
		f_rf= open("/home/mininet/Escritorio/scripts/output/dl.txt","w+")
		f_rf.close()
	
	f_datosML3= open("/home/mininet/Escritorio/scripts/output/datosML3.txt","w+")
	f_datosML3.write("{},{},{},{},{},{},{}\n".format("station", "ap", "rssi", "num_sta", "dist", "cons_bat", "associatedTo"))
	f_datosML3.close()
	
	f_datosML4= open("/home/mininet/Escritorio/scripts/output/datosML4.txt","w+")
	f_datosML4.write("{},{},{},{},{},{},{}\n".format("station","aps", "ap", "rssi", "num_sta", "dist", "cons_bat", "associatedTo"))
	f_datosML4.close()
	
	f_datosML5= open("/home/mininet/Escritorio/scripts/output/datosML5.txt","w+")
	f_datosML5.write("{},{},{},{},{},{},{}\n".format("station","aps", "ap", "rssi", "num_sta", "dist", "cons_bat", "associatedTo"))
	f_datosML5.close()
	
	f_stations_info= open("/home/mininet/Escritorio/scripts/output/f_stations_info.txt","w+")
	f_stations_info.write('{},{},{},{},{}\n'.format("station", "associatedTo","battery", "rssi", "position"))
	#f_stations_info.write("{},{},{},{},{},{},{}\n".format("station","aps", "ap", "rssi", "num_sta", "dist", "cons_bat", "associatedTo"))
	f_stations_info.close()
	
	info("*** Creating nodes\n")
	
	"""
	sta1 = net.addStation('sta1', ip='10.0.1.123', mac='00:00:00:02:09:01', position='40.48,100.36,0.00', range = 20, speed=1, bw_d = 2000, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","",""]])
	sta2 = net.addStation('sta2', ip='10.0.1.2', mac='00:00:00:01:09:02', position='30.0,180.0,0', range = 20, speed=1, bw_d = 2500, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","",""]])
	sta3 = net.addStation('sta3', ip='10.0.1.3', mac='00:00:00:02:09:03', position='50.0,125.0,0', range = 20, speed=1, bw_d = 2000, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","",""]])
	sta4 = net.addStation('sta4', ip='10.0.1.4', mac='00:00:00:03:09:04', position='125.0,110.0,0', range = 20, speed=1, bw_d = 2000, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","",""]])
	
	"""
	sta1 = net.addStation('sta1', ip='10.0.1.123', mac='00:00:00:02:09:01', position='40.48,100.36,0.00', range = 20, speed=1, bw_d = 2000, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","","","","","",""]])
	sta2 = net.addStation('sta2', ip='10.0.1.2', mac='00:00:00:01:09:02', position='30.0,180.0,0', range = 20, speed=1, bw_d = 2500, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","","","","","",""]])
	sta3 = net.addStation('sta3', ip='10.0.1.3', mac='00:00:00:02:09:03', position='50.0,125.0,0', range = 20, speed=1, bw_d = 2000, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","","","","","",""]])
	sta4 = net.addStation('sta4', ip='10.0.1.4', mac='00:00:00:03:09:04', position='125.0,110.0,0', range = 20, speed=1, bw_d = 2000, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","","","","","",""]])
	
    
	u1_d1 = net.addStation('u1_d1', ip='10.0.0.134', mac='01:01:01:00:01:01', position='10.0,150.0,0', range = 20, speed = 1, battery = 100, bw_d = 2000)
	u1_d2 = net.addStation('u1_d2', ip='10.0.0.2', mac='02:01:02:00:01:02', position='10.0,150.0,0', range = 20, speed = 1, battery = 100, bw_d = 2000)
	u1_d3 = net.addStation('u1_d3', ip='10.0.0.3', mac='03:01:03:00:01:03', position='10.0,150.0,0', range = 20, speed = 1, battery = 100, bw_d = 2000)
	
	u2_d1 = net.addStation('u2_d1', ip='10.0.0.4', mac='01:02:03:00:02:01', position='90.0,210.0,0', range = 20, speed = 2, battery = 100, bw_d = 2000)
	u2_d2 = net.addStation('u2_d2', ip='10.0.0.5', mac='02:02:03:00:02:02', position='90.0,210.0,0', range = 20, speed = 2, battery = 100, bw_d = 2000)
	u2_d3 = net.addStation('u2_d3', ip='10.0.0.6', mac='03:02:01:00:02:03', position='90.0,210.0,0', range = 20, speed = 2, battery = 100, bw_d = 2000)
	u2_d4 = net.addStation('u2_d4', ip='10.0.0.7', mac='04:02:04:00:02:04', position='90.0,210.0,0', range = 20, speed = 2, battery = 100, bw_d = 2000)
	
	
	#AP4
	sta9 = net.addStation('sta9', ip='10.0.1.9', mac='00:00:00:00:09:09', position='75.0,75.0,0', range = 20, battery = 100, bw_d = 2000)
	sta10 = net.addStation('sta10', ip='10.0.1.10', mac='00:00:00:00:09:10', position='35.0,95.0,0', range = 20, battery = 100, bw_d = 2000)
	
	#AP3
	"""
	sta5 = net.addStation('sta5', ip='10.0.1.5', mac='00:00:00:03:09:05', position='90.0,70.0,0', range = 20, speed=1, bw_d = 1000, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","",""]])
	sta6 = net.addStation('sta6', ip='10.0.1.6', mac='00:00:00:03:09:06', position='125.0,180.0,0', range = 20, speed=1, bw_d = 2000, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","",""]])
	sta7 = net.addStation('sta7', ip='10.0.1.7', mac='00:00:00:01:09:07', position='110.0,170.0,0', range = 20, speed=1, bw_d = 1500, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","",""]])
	sta8 = net.addStation('sta8', ip='10.0.1.8', mac='00:00:00:02:09:08', position='91.0,175.0,0', range = 20, speed=1, bw_d = 2000, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","",""]])
	"""
	
	sta11 = net.addStation('sta11', ip='10.0.1.11', mac='01:00:00:00:09:10', position='160.0,150.0,0', range = 20, battery = 100, bw_d = 2000)
	
	sta5 = net.addStation('sta5', ip='10.0.1.5', mac='00:00:00:03:09:05', position='90.0,70.0,0', range = 20, speed=1, bw_d = 1000, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","","","","","",""]])
	sta6 = net.addStation('sta6', ip='10.0.1.6', mac='00:00:00:03:09:06', position='125.0,180.0,0', range = 20, speed=1, bw_d = 2000, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","","","","","",""]])
	sta7 = net.addStation('sta7', ip='10.0.1.7', mac='00:00:00:01:09:07', position='110.0,170.0,0', range = 20, speed=1, bw_d = 1500, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","","","","","",""]])
	sta8 = net.addStation('sta8', ip='10.0.1.8', mac='00:00:00:02:09:08', position='91.0,175.0,0', range = 20, speed=1, bw_d = 2000, battery = 100, id_group = "", hist = [[0, 0, 0],[0, 0, 0],["","",""],["","","","","","","","","","","","","",""]])
	
	
	#ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1', position='45,45,0')
	
	info( '*** Add switches/APs\n')
	ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='n', channel='1', position='50.0,150.0,0', antennaGain = 5, range = 45, battery = 100, maxDis = 15, bw_ap = 15000) # gain 8 = (txpow = 3 + gain = 5)
	ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='n', channel='7', position='90.0,180.0,0', antennaGain = 6, range = 50, battery = 100, maxDis = 18, bw_ap = 17000)# gain 3 = ( gain = 3)
	ap3 = net.addAccessPoint('ap3', ssid='ap3-ssid', mode='n', channel='11', position='130.0,150.0,0', antennaGain = 5, range=45, battery = 100, maxDis = 15, bw_ap = 15000) # gain 7 = (txpow = 2 + gain = 5)
	ap4 = net.addAccessPoint('ap4', ssid='ap4-ssid', mode='n', channel='11', position='90.0,90.0,0', antennaGain = 6, range=57, battery = 100, maxDis = 20, bw_ap = 15000) # gain 10 = (txpow = 4 + gain = 6)
	s1 = net.addSwitch('s1')

	info("*** Configuring Propagation Model\n")
	#net.setPropagationModel(model="logDistance", exp=4.5)

	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	info("*** Creating links\n")
	#net.addLink(sta3, cls=adhoc, ssid='adhocNet')
	#net.addLink(sta4, cls=adhoc, ssid='adhocNet')
	info( '*** Add links\n')

	net.addLink(s1, ap1)
	net.addLink(s1, ap2)
	net.addLink(s1, ap3)
	net.addLink(s1, ap4)
	
	
	path = os.path.dirname(os.path.abspath(__file__))
	
	getTrace2(sta1, '%s/replayingMobility/u10_mov.txt' % path, net)
	getTrace2(sta2, '%s/replayingMobility/u10_mov.txt' % path, net)
	getTrace2(sta3, '%s/replayingMobility/u10_mov.txt' % path, net)
	getTrace2(sta4, '%s/replayingMobility/u10_mov.txt' % path, net)
	
	
	getTrace3(sta5, '%s/replayingMobility/u10_mov.txt' % path, net)
	getTrace3(sta6, '%s/replayingMobility/u10_mov.txt' % path, net)
	getTrace3(sta7, '%s/replayingMobility/u10_mov.txt' % path, net)
	getTrace3(sta8, '%s/replayingMobility/u10_mov.txt' % path, net)
	
	
	net.plotGraph(max_x=180, max_y=250)
	
	print "*** Enabling association control (AP)"
	net.setAssociationCtrl(asoc)
	time.sleep(5)

	info("*** Starting network\n")
	net.build()
	net.start()
	
	ap1.setTxPower(3, intf='ap1-wlan1')
	ap2.setTxPower(4, intf='ap2-wlan1')
	ap3.setTxPower(2, intf='ap3-wlan1')
	ap4.setTxPower(4, intf='ap4-wlan1')
	
	"""
	#Prueba iperf
	print("creando terminales grupo 1")
	makeTerm( sta10, cmd="bash -c 'iperf -s -u -p 5566 -i 1 > resultiperf_group1_sta1;'" )
	#makeTerm( sta9, cmd="bash -c 'iperf -s -u -p 5566 -i 1 > resultiperf_sta2;'" )
	time.sleep(1)
	makeTerm( sta1, cmd="bash -c 'iperf -c 10.0.1.10 -u -b 1M -t 600 -p 5566;'" )
	#makeTerm( sta2, cmd="bash -c 'iperf -c 10.0.1.9 -u -b 1M -t 600 -p 5566;'" )
	#makeTerm( sta3, cmd="bash -c 'iperf -c 10.0.1.9 -u -b 1M -t 600 -p 5566;'" )
	#makeTerm( sta4, cmd="bash -c 'iperf -c 10.0.1.9 -u -b 1M -t 600 -p 5566;'" )
	#makeTerm( sta2, cmd="bash -c 'iperf -c 10.0.1.9 -u -b 2M -t 1000 -p 5566;'" )
	print("terminales creandos grupo 1")
	
	#Prueba iperf
	print("creando terminales grupo 2")
	makeTerm( u1_d2, cmd="bash -c 'iperf -s -u -p 5566 -i 1 > resultiperf_group2_sta5;'" )
	#makeTerm( sta9, cmd="bash -c 'iperf -s -u -p 5566 -i 1 > resultiperf_sta2;'" )
	time.sleep(1)
	makeTerm( sta5, cmd="bash -c 'iperf -c 10.0.0.2 -u -b 1M -t 600 -p 5566;'" )
	#makeTerm( sta6, cmd="bash -c 'iperf -c 10.0.0.5 -u -b 1M -t 600 -p 5566;'" )
	#makeTerm( sta7, cmd="bash -c 'iperf -c 10.0.0.5 -u -b 1M -t 600 -p 5566;'" )
	#makeTerm( sta8, cmd="bash -c 'iperf -c 10.0.0.5 -u -b 1M -t 600 -p 5566;'" )
	#makeTerm( sta2, cmd="bash -c 'iperf -c 10.0.1.9 -u -b 2M -t 1000 -p 5566;'" )
	print("terminales creandos grupo 2")
	"""
	print("tiempo iniciado")
	time.sleep(20)
	
	replayingMobility(net)
	print("tiempo iniciado2")
	time.sleep(20)
	
	info("*** Running CLI\n")
	CLI_wifi(net)

	info("*** Stopping network\n")
	net.stop()

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
		x = line[0]  # First Column
		y = line[1]  # Second Column
		pos = float(x),float(y),0.0
		sta.position.append(pos)

def getTrace2(sta, file_, net):
	net.isReplaying = True
	file_ = open(file_, 'r')
	raw_data = file_.readlines()
	file_.close()
	sta.position = []
	pos = '-1000,0,0'
	sta.params['position'] = [float(x) for x in pos.split(',')]
	for data in raw_data:
		line = data.split()
		pos2 = line[1]
		line2= pos2.split(',')
		x = line2[0]  # First Column
		y = line2[1]  # Second Column
		pos = float(x),float(y),0.0
		sta.position.append(pos)
		
def getTrace3(sta, file_, net):
	net.isReplaying = True
	file_ = open(file_, 'r')
	raw_data = file_.readlines()
	file_.close()
	sta.position = []
	pos = '-1000,0,0'
	sta.params['position'] = [float(x) for x in pos.split(',')]
	for data in raw_data:
		line = data.split()
		print(line)
		pos2 = line[3]
		line2= pos2.split(',')
		x = line2[0]  # First Column
		y = line2[1]  # Second Column
		pos = float(x),float(y),0.0
		sta.position.append(pos)
if __name__ == '__main__':
	setLogLevel('info')
	topology()
