import os, socket, re, time, pcap, dpkt, threading, pika

for ts, pkt in pcap.pcap("files/test.pcap"):
    protocolos = ["http","dhcp","bittorrent","ssdp","ssl","ssh"]
    eth = dpkt.ethernet.Ethernet(pkt)
    ip = eth.data
    if isinstance(ip,dpkt.ip.IP):
        print "IP"
        transp = ip.data
        if isinstance(transp,dpkt.tcp.TCP):
            print "TCP"
        elif isinstance(transp,dpkt.udp.UDP):
            print "UDP"
        app = transp.data.lower()
        for p in protocolos:
            parametro = "dkpt."+p+"."+p.upper()
            if isinstance(app,parametro):
                print p
    else:
        print "Nao eh IP"