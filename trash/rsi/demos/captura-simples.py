import pcap, dpkt

maxPkts = 10
nPkts=0

for ts, pkt in pcap.pcap():
	nPkts += 1

	print("Pacote puro #"+str(nPkts))
	print(dpkt.hexdump(pkt))

	print("Mostrando o pacote #"+str(nPkts))
	eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
	print(ts, repr(eth))
	print("Mostrando o endereco de destino do pacote #"+str(nPkts))
	print(repr(eth.dst))
	print("\n")

	if (nPkts == maxPkts):
		break
