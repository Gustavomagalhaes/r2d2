import atexit
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import info,setLogLevel

net = None

def createTopo():
	topo=Topo()
	#Create Nodes
	topo.addHost("h1")
	topo.addHost("h2")
	topo.addHost("h3")
	topo.addHost("h4")
	topo.addSwitch('s1')
	topo.addSwitch('s2')
	topo.addHost("r1") #router
	#Create links
	topo.addLink('h1','s1')	
	topo.addLink('h2','s1')	
	topo.addLink('s1','r1')	
	topo.addLink('s2','r1')	
	topo.addLink('h3','s2')	
	topo.addLink('h4','s2')	
	return topo

def startNetwork():
	topo = createTopo()
	global net
	net = Mininet(topo=topo, autoSetMacs=True)
	net.start()
	h1,h2,h3,h4,r1  = net.hosts[0],net.hosts[1],net.hosts[2],net.hosts[3],net.hosts[4]
	h1.cmd('ifconfig h1-eth0 0.0.0.0')
	h2.cmd('ifconfig h2-eth0 0.0.0.0')
	h3.cmd('ifconfig h3-eth0 0.0.0.0')
	h4.cmd('ifconfig h4-eth0 0.0.0.0')
	r1.cmd('ifconfig r1-eth0 0.0.0.0')
	r1.cmd('ifconfig r1-eth1 0.0.0.0')
	CLI(net)

def stopNetwork():
	if net is not None:
		net.stop()

if __name__ == '__main__':
	atexit.register(stopNetwork)
	setLogLevel('info')
	startNetwork()
