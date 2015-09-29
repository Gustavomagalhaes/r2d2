# -*- coding: utf-8 -*-
import os, time, socket, threading, Queue, pika, datetime
import pcap, dpkt, re

class Thread(threading.Thread):
    
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.status = None
        self.contProtocolos = {"http":0, "ssdp":0, "ssl":0, "dhcp":0, "ssh":0, "unknown":0, "all":0, "nonIp":0}
        self.cNonIP = 0
        
    def listarProtocolos(self):
            # diretorio = os.listdir(os.getcwd()+'//l7-pat')
            # protocolos = {}
    
            # for arquivo in diretorio:
            #     arquivo = './/l7-pat//'+ arquivo 
    
            #     file = open(arquivo, 'r')
            #     linha = file.readline()
                
            #     while linha != "":        
            #         if linha[0] != "#":
            #             if linha[0] != "^" and linha[:5] != "http/" and linha[0] != "\n":
            #                 chave = str(linha.replace("\n",""))
            #             elif  (linha[0] == "^" or linha[:5] == "http/") and linha[0] != "\n":
            #                 valor = (str(linha).lstrip()).rstrip()
            #         linha = file.readline()
                    
            #     protocolos[chave] = re.compile(valor)
            protocolos = {"dhcp":"^[\x01\x02][\x01- ]\x06.*c\x82sc","http":"[\x09-\x0d -~]*"}
                
            return protocolos

    def descobrirProtocolo(self, transp):
        if isinstance(transp,dpkt.udp.UDP):
            retorno = "TCP"
        elif isinstance(transp,dpkt.tcp.TCP):
            retorno = "UDP"
        else:
            retorno = "Nenhum"
        return retorno

    def extrairPacotes(self):
        protocolos = self.listarProtocolos()
        for ts, pkt in pcap.pcap("test.pcap"):
            eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
            ip = eth.data
            if isinstance(ip,dpkt.ip.IP):
                transp = ip.data
                if isinstance(transp,dpkt.tcp.TCP) or isinstance(transp,dpkt.udp.UDP):
                    app = transp.data.lower()
                    found = False
                    for p in protocolos.items():
                        expressao = re.compile(p[1])
                        if expressao.search(app):
                            print str(p[1])
                            self.contProtocolos[p[0]] += 1
                            found = True
        					
                        if (not found):
                            self.contProtocolos["unknown"] += 1
            else:
                self.contProtocolos["nonIp"] += 1
        
        for p in self.contProtocolos.items():
        	print(p[0]+" Pkts:"+str(p[1]))
        
if __name__ == '__main__':
    thread = Thread()
    thread.extrairPacotes()