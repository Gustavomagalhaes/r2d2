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
	topo.addHost("h5")
	topo.addHost("h6")
	topo.addSwitch('s1')
	topo.addSwitch('s2')
	topo.addSwitch('s3')
	topo.addHost("r1") #router
	topo.addHost("r2") #router
	topo.addHost("r3") #router
	#Create links
	topo.addLink('h1','s1')	
	topo.addLink('h2','s1')	
	topo.addLink('s1','r1')	
	topo.addLink('h3','s2')	
	topo.addLink('h4','s2')	
	topo.addLink('s2','r2')
	topo.addLink('h5','s3')	
	topo.addLink('h6','s3')	
	topo.addLink('s3','r3')
	topo.addLink('r1','r2')
	topo.addLink('r1','r3')
	topo.addLink('r2','r3')
	return topo

def startNetwork():
	topo = createTopo()
	global net
	net = Mininet(topo=topo, autoSetMacs=True)
	net.start()
	h1,h2,h3,h4,h5,h6,r1,r2,r3  = net.hosts
	h1.cmd('ifconfig h1-eth0 10.0.0.1 netmask 255.255.255.0')
	h1.cmd('route add default gw 10.0.0.3')
	h2.cmd('ifconfig h2-eth0 10.0.0.2 netmask 255.255.255.0')
	h2.cmd('route add default gw 10.0.0.3')
	h3.cmd('ifconfig h3-eth0 20.0.0.1 netmask 255.255.255.0')
	h3.cmd('route add default gw 20.0.0.3')
	h4.cmd('ifconfig h4-eth0 20.0.0.2 netmask 255.255.255.0')
	h4.cmd('route add default gw 20.0.0.3')
	h5.cmd('ifconfig h5-eth0 30.0.0.1 netmask 255.255.255.0')
	h5.cmd('route add default gw 30.0.0.3')
	h6.cmd('ifconfig h6-eth0 30.0.0.2 netmask 255.255.255.0')
	h6.cmd('route add default gw 30.0.0.3')

	r1.cmd('ifconfig r1-eth0 10.0.0.3 netmask 255.255.255.0')
	r2.cmd('ifconfig r2-eth0 20.0.0.3 netmask 255.255.255.0')
	r3.cmd('ifconfig r3-eth0 30.0.0.3 netmask 255.255.255.0')

	r1.cmd('ifconfig r1-eth1 110.0.0.1 netmask 255.255.255.0')
	r2.cmd('ifconfig r2-eth1 110.0.0.2 netmask 255.255.255.0')
	r1.cmd('ifconfig r1-eth2 120.0.0.1 netmask 255.255.255.0')
	r3.cmd('ifconfig r3-eth1 120.0.0.2 netmask 255.255.255.0')
	r2.cmd('ifconfig r2-eth2 130.0.0.1 netmask 255.255.255.0')
	r3.cmd('ifconfig r3-eth2 130.0.0.2 netmask 255.255.255.0')

	r1.cmd('echo 1 >> /proc/sys/net/ipv4/ip_forward')
	r2.cmd('echo 1 >> /proc/sys/net/ipv4/ip_forward')
	r3.cmd('echo 1 >> /proc/sys/net/ipv4/ip_forward')

	CLI(net)

def stopNetwork():
	if net is not None:
		info('** Tearing down the network\n')
		net.stop()

if __name__ == '__main__':
	atexit.register(stopNetwork)
	setLogLevel('info')
	startNetwork()
