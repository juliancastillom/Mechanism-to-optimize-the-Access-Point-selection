#!/usr/bin/python

'Un dispositivo se mueve por tres AP'

from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import TCLink
from mn_wifi.node import OVSKernelAP
from mininet.cli import CLI
from mn_wifi.cli import CLI_wifi
from mininet.log import setLogLevel
from mn_wifi.net import Mininet_wifi

def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=TCLink, accessPoint=OVSKernelAP)

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8')
    """sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8')
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8')
    sta4 = net.addStation('sta4', mac='00:00:00:00:00:05', ip='10.0.0.5/8')
    sta5 = net.addStation('sta5', mac='00:00:00:00:00:06', ip='10.0.0.6/8')
    sta6 = net.addStation('sta6', mac='00:00:00:00:00:07', ip='10.0.0.7/8')
    sta7 = net.addStation('sta7', mac='00:00:00:00:00:08', ip='10.0.0.8/8')
    sta8 = net.addStation('sta8', mac='00:00:00:00:00:09', ip='10.0.0.9/8')
    sta9 = net.addStation('sta9', mac='00:00:00:00:00:10', ip='10.0.0.10/8')
    sta10 = net.addStation('sta10', mac='00:00:00:00:00:11', ip='10.0.0.11/8')"""
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='30,50,0', range=20)
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='6', position='60,50,0', range=20)  # range: set the AP range
    ap3 = net.addAccessPoint('ap3', ssid='ssid-ap3', mode='g', channel='11', position='90,50,0', range=20)
    c1 = net.addController('c1', controller=Controller)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Associating and Creating links"
    net.addLink(ap1, ap2)
    net.addLink(ap2, ap3)

    """plotting graph"""
    net.plotGraph(max_x=130, max_y=100)

    """association control"""
    #net.associationControl('ssf')

    """Seed"""
    #net.seed(1)

    """ *** Available models:
                RandomWalk, TruncatedLevyWalk, RandomDirection, RandomWayPoint, GaussMarkov
    *** Association Control (AC) - mechanism that optimizes the use of the APs:
                llf (Least-Loaded-First)
                ssf (Strongest-Signal-First)"""
    net.startMobility( time=0, associationControl= 'ssf', seed =100)
    #net.startMobility(time=0, model='RandomWayPoint', max_x=120, max_y=100, min_v=0.8, max_v=2, seed=1, associationControl='ssf')

    net.mobility( sta1, 'start', time=1, position='10,50,0' )
    net.mobility( sta1, 'stop', time=19, position='120,100,0' )
    net.stopMobility( time=20 )
    #net.startMobility(time=0, model='RandomWayPoint', max_x=120, max_y=100, min_v=0.8, max_v=2, AC='llf')

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
topology()
