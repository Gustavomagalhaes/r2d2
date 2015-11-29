# -*- coding: utf-8 -*-
import os, socket, re, time, pcap, dpkt, threading, pika

class Various():
    
    def __init__(self):
        
        self.status = None
        self.pacotes = {}
        self.contProtocolos = {"http":0, "ssdp":0, "ssl":0, "dhcp":0, "ssh":0, "nbns":0, "dropbox":0, "unknown":0, "all":0, "nonIp":0}
        #self.run()
        
    def getPacotes(self):
        return self.pacotes
        
    def setPacote(self, chave, conteudo):
        self.pacotes[(chave)] = conteudo
        
    def getStatus(self):
        return self.status
        
    def setStatus(self, status):
        self.status = status
        
    def getcontProtocolos(self):
        return self.contProtocolos
        
    def run(self):
        print "Tá no run"
        yoda = threading.Thread(target=self.iniciarColeta("",10000))
        yoda.start()
    
    def listarProtocolos(self):
            diretorio = os.listdir(os.getcwd()+'/l7-pat')
            protocolos = {}
                
            for arquivo in diretorio:
                arquivo = 'l7-pat/'+ arquivo 
                
                file = open(arquivo, 'r')
                linha = file.readline()
                
                while linha != "":        
                    if linha[0] != "#":
                        if linha[0] != "^" and linha[:5] != "http/" and linha[0] != "\n":
                            chave = str(linha.replace("\n",""))
                        elif  (linha[0] == "^" or linha[:5] == "http/") and linha[0] != "\n":
                            valor = (str(linha).lstrip()).rstrip()
                    linha = file.readline()
                                
                #protocolos[chave] = re.compile(valor)
                #valor = re.compile(valor)
                proto = {}
                arq = open("protocolos.txt","r")
                listaLinhas = arq.readlines()
                for linha in listaLinhas:
                    linha = linha.split(":")
                    expr = linha[1].replace("\n","")
                    nome= linha[0]
                    proto[nome] = re.compile(expr)
                for p in proto.iteritems():
                    if chave == p[0]:
                        print chave + "\t" + str(p[0])
                        print "ARQUIVO:\t" + str(re.compile(valor))
                        print "DICIONARIO:\t" + str(p[1])
                protocolos[chave] = valor
            #protocolos = {"ssl":"^(.?.?\x16\x03.*\x16\x03|.?.?\x01\x03\x01?.*\x0b)", "ssh":"^ssh-[12]\.[0-9]", "ssdp":"^notify[\x09-\x0d ]\*[\x09-\x0d ]http/1\.1[\x09-\x0d -~]*ssdp:(alive|byebye)|^m-search[\x09-\x0d ]\*[\x09-\x0d ]http/1\.1[\x09-\x0d -~]*ssdp:discover", "bittorrent":"^(\x13bittorrent protocol|azver\x01$|get /scrape\?info_hash=)", "dhcp":"^[\x01\x02][\x01- ]\x06.*c\x82sc", "http":"[\x09-\x0d -~]*"}
                
            return protocolos
            
    def classificarProtocolo(self, protocolo):
        for nome, p in self.listarProtocolos().iteritems():
            p = re.compile(p)
            if p.search(protocolo):            
                return nome
        return "unknown"
            
    def enviarFila(self, routing_key, mensagem):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
               "", 5672, '/starwars', pika.PlainCredentials("skywalker", "luke")))
        channel = connection.channel()
        channel.exchange_declare(exchange='topic_logs',type='topic')
        channel.basic_publish(exchange='topic_logs',routing_key=routing_key,body=mensagem)
        
        print " [x] Sent %r:%r" % (routing_key, mensagem)
        
        connection.close()
    
    def iniciarColeta(self, file="", tempo = 60):
        protocols = self.listarProtocolos()
        cnt = self.getcontProtocolos()
        cNonIP = 0
        
        for ts, pkt in pcap.pcap(file):
        
        	eth = dpkt.ethernet.Ethernet(pkt)
        	ip = eth.data
        	if isinstance(ip,dpkt.ip.IP):
        		transp = ip.data
        		if isinstance(transp,dpkt.tcp.TCP) or isinstance(transp,dpkt.udp.UDP):
        			app = transp.data.lower()
        			found = False
        			for p in protocols.items():
        				if re.compile(p[1]).search(app):
        					cnt[p[0]] += 1
        					print p[0] + str(ts)
        					cnt["all"] += 1
        					found = True
        			if (not found):
        				cnt["unknown"] += 1
        				print "unkown"
        				cnt["all"] += 1
        	else:
        		cNonIP += 1
        		cnt["all"] += 1
        
        for p in cnt.items():
        	print(p[0]+" Pkts:"+str(p[1]))
        print("Non IP Pkts:"+str(cNonIP))

if __name__ == '__main__':
    
    various = Various()
    various.listarProtocolos()
    