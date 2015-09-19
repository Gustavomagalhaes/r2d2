import pcap, dpkt, socket

nPkts=0

for ts, pkt in pcap.pcap("web.pcap"):
	nPkts += 1
	eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
	ip = eth.data
	tcp = eth.data.data

	print(str(nPkts)+" "+socket.inet_ntoa(ip.src)+" "+socket.inet_ntoa(ip.dst)+" "+repr(tcp.sport)+" "+repr(tcp.dport)+" "+repr(ip.len)+" "+repr(tcp.flags))
	print("\n")
	
	#print("Pacote puro #"+str(nPkts))
	#print(dpkt.hexdump(pkt))

	
	

