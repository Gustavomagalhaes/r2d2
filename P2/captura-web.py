# Made by Gustavo Magalhaes
import pcap, dpkt, socket

nPkts=0

for ts, pkt in pcap.pcap("web.pcap"):
	nPkts += 1
	eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
	ip = eth.data
	tcp = eth.data.data
	print(str(nPkts)+"\t"+socket.inet_ntoa(ip.src)+"\t"+socket.inet_ntoa(ip.dst)+"\t"+repr(tcp.sport)+"\t"+repr(tcp.dport)+"\t"+str(len(pkt))+"\t"+str(len(tcp.data))+"\t"+str(len(pkt)-len(tcp.data)))
		
	
	#print("Pacote puro #"+str(nPkts))
	#print(dpkt.hexdump(pkt))
	
	#print("\n")
	#print (repr(eth))
	#print "\n"
	#print "Pacote completo: "
	#print(len(pkt))
	#print "Pacote sem cabecalhos: "
	#print(len(tcp.data))

	
