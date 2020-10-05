#!/usr/bin/python

from mn_wifi.net import Mininet_wifi
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from functools import partial

from mininet.node import Controller, RemoteController, OVSKernelSwitch, OVSSwitch
from mininet.link import TCLink

def emptyNet():

    "Create an empty network and add nodes to it."
    info( '*** Adding controller\n' )
    net = Mininet_wifi( listenPort = 6633,topo=None)
    #net = Mininet_wifi( topo=None,build=False,link=wmediumd,wmediumd_mode=interference,ipBase='10.0.0.0/8')

    #mycontroller = RemoteController("remoteController",ip="192.168.238.129")
    #mycontroller = RemoteController("remoteController",ip="127.0.0.1")
    #net.controllers = [mycontroller]
    #net.nameToNode["remoteController"] = mycontroller
    
    info( '*** Adding controller\n' )
    mycontroller=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='192.168.0.1/24', mac='00:00:00:00:00:01' )
    h2 = net.addHost( 'h2', ip='192.168.0.2/24', mac='00:00:00:00:00:02' )

    sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:03', ip="192.168.0.3/24" ,range='5' )
    sta2 = net.addStation( 'sta2', mac='00:00:00:00:00:08', ip="192.168.0.8/24" ,range='5', position='5,10,0' )

    ap1 = net.addAccessPoint( 'ap1', ssid= 'ap-ssid', dpid='0000000100000001',mode= 'g', channel= '1', position='10,10,0', range='10' )
    ap2 = net.addAccessPoint( 'ap2', ssid= 'ap-ssid', dpid='0000000100000002', mode= 'g', channel= '1', position='25,10,0', range='10' )
    ap3 = net.addAccessPoint( 'ap3', ssid= 'ap-ssid', dpid='0000000100000003',mode= 'g', channel= '1', position='40,10,0', range='10' )

    info( '*** Adding switch\n' )
    s1 = net.addSwitch('s1',dpid='0000000100000004')
    s2 = net.addSwitch('s2',dpid='0000000100000005')
    s3 = net.addSwitch('s3',dpid='0000000100000006')
    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    net.addLink(s1, ap1, 1, 2)# node1,   node2, port1, port2
    net.addLink(s1, ap2, 2, 2)
    net.addLink(s1, h1, 3, 1)

    net.addLink(s2, s1, 1, 4)
    net.addLink(s2, s3, 2, 1)
    net.addLink(s3, ap3, 2, 2)

    net.addLink(s3, h2)

    net.plotGraph(max_x=50, max_y=50)
    #net.startMobility(startTime=20, AC='ssf')
    net.startMobility( time=0, AC='ssf')
    net.mobility( sta1, 'start', time=20, position='20,10,0' )
    net.mobility( sta1, 'stop', time=70, position='50,10,0' )
    net.stopMobility( time=70 )
    #net.mobility(sta1, 'start', time=20, position='1,10,0')
    #net.mobility(sta1, 'stop', time=120, position='160,50,0')
    #net.mobility(sta1, 'stop', time=70, position='50,10,0')
    #net.stopMobility(stopTime=70) 

    #set the bw loss delay and so on 
    net.setChannelEquation(bw='5', loss='0', delay='0', latency='0')
    info( '*** Starting network\n')
    net.start()

    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()
