import pcap, dpkt

nPkts=0

for ts, pkt in pcap.pcap("web.pcap"):
	nPkts += 1
	eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
	
	print("No., Dport, sport")
	print(str(nPkts)+" "+repr(eth.data.data.dport)+" "+repr(eth.data.data.sport))

	#print("Pacote puro #"+str(nPkts))
	#print(dpkt.hexdump(pkt))

	#print("Mostrando o pacote #"+str(nPkts))
	print("\n")
	print(ts, repr(eth))
	print("\n")
	#print("Mostrando o endereco de destino do pacote #"+str(nPkts))
	#print(repr(eth.dst))
	#print("\n")
	
	

