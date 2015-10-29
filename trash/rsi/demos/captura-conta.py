import pcap, dpkt

#contadores
cNonIP = 0
cUDP = 0
cTCP = 0

for ts, pkt in pcap.pcap("test.pcap"):

	eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
	if isinstance(eth.data,dpkt.ip.IP):
		ip = eth.data
		if isinstance(ip.data,dpkt.tcp.TCP):
			cTCP += 1
		elif isinstance(ip.data,dpkt.udp.UDP):
			cUDP += 1
	else:
		cNonIP += 1

print("IP Pkts:"+str(cTCP+cUDP))
print("TCP Pkts:"+str(cTCP))
print("UDP Pkts:"+str(cUDP))
print("Non IP Pkts:"+str(cNonIP))
