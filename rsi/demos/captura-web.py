import pcap, dpkt, socket

nPkts=0

for ts, pkt in pcap.pcap("web.pcap"):
	nPkts += 1
	eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
	ip = eth.data
	tcp = eth.data.data
	#print(str(nPkts)+"\t"+socket.inet_ntoa(ip.src)+"\t"+socket.inet_ntoa(ip.dst)+"\t"+repr(tcp.sport)+"\t"+repr(tcp.dport)+"\t"+repr(ip.len)+"\t"+repr(tcp.flags))
	print(str(nPkts)+"\t"+socket.inet_ntoa(ip.src)+"\t"+socket.inet_ntoa(ip.dst)+"\t"+repr(tcp.sport)+"\t"+repr(tcp.dport)+"\t"+pcap.len)
	
	if (nPkts == 198) :
		print(pcap.len)
	
	
	#print("Pacote puro #"+str(nPkts))
	#print(dpkt.hexdump(pkt))
	
	