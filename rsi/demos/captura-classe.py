import pcap, dpkt, re

#assinaturas de protocolos de camada de aplicacao
expr="\x01\x10\x00\x01"
nbns = re.compile(expr)
expr="^\x7b\x22\x68\x6f"
dropbox = re.compile(expr)
expr="^[\x01\x02][\x01- ]\x06.*c\x82sc"
dhcp = re.compile(expr)

protocols = {"dropbox":dropbox,"nbns":nbns,"dhcp":dhcp}

#contadores
cnt = {"dropbox":0,"nbns":0,"dhcp":0,"noClass":0}
cNonIP = 0

for ts, pkt in pcap.pcap("test.pcap"):

	eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
	ip = eth.data
	if isinstance(ip,dpkt.ip.IP):
		transp = ip.data
		if isinstance(transp,dpkt.tcp.TCP) or isinstance(transp,dpkt.udp.UDP):
			app = transp.data.lower()
			found = False
			for p in protocols.items():
				if p[1].search(app):
					cnt[p[0]] += 1
					found = True
			if (not found):
				cnt["noClass"] += 1
	else:
		cNonIP += 1

for p in cnt.items():
	print(p[0]+" Pkts:"+str(p[1]))
print("Non IP Pkts:"+str(cNonIP))
