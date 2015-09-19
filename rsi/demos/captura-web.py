import pcap, dpkt

nPkts=0

for ts, pkt in pcap.pcap("web.pcap"):
	nPkts += 1
	eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
	ip = eth.data
	tcp = eth.data.data
	
	print("IP source e IP Dest")
	print(repr(eth.src)+" "+repr(eth.dst))

	print("\n")

	print("No., TCP origem, TCP destino , tamanho IP, tamanho TCP")
	print(str(nPkts)+" "+repr(tcp.sport)+" "+repr(tcp.dport)+" "+repr(ip.len)+" "+repr(tcp.flags))

	#print("Pacote puro #"+str(nPkts))
	#print(dpkt.hexdump(pkt))

	#print("Mostrando o pacote #"+str(nPkts))
	print("\n")
	print(ts, repr(eth))
	print("\n")
	#print("Mostrando o endereco de destino do pacote #"+str(nPkts))
	#print(repr(eth.dst))
	#print("\n")
	
	

