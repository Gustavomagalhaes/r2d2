# -*- coding: utf-8 -*-
import os, socket, re, time, pcap, dpkt, threading, pika

class Various():
    
    def __init__(self):
        
        self.status = None
        self.pacotes = {}
        self.contProtocolos = self.contProtocolos = {"http":0, "ssdp":0, "ssl":0, "dhcp":0, "ssh":0, "unknown":0, "all":0, "nonIp":0}
        self.run()
        
    def getPacotes(self):
        return self.pacotes
        
    def setPacote(self, chave, conteudo):
        self.pacotes[(chave)] = conteudo
        
    def getStatus(self):
        return self.status
        
    def setStatus(self, status):
        self.status = status
        
    def run(self):
        print "Tá no run"
        yoda = threading.Thread(target=self.iniciarColeta("files/test.pcap",10000))
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
                                
                protocolos[chave] = re.compile(valor)
            #protocolos = {"ssl":"^(.?.?\x16\x03.*\x16\x03|.?.?\x01\x03\x01?.*\x0b)", "ssh":"^ssh-[12]\.[0-9]", "ssdp":"^notify[\x09-\x0d ]\*[\x09-\x0d ]http/1\.1[\x09-\x0d -~]*ssdp:(alive|byebye)|^m-search[\x09-\x0d ]\*[\x09-\x0d ]http/1\.1[\x09-\x0d -~]*ssdp:discover", "bittorrent":"^(\x13bittorrent protocol|azver\x01$|get /scrape\?info_hash=)", "dhcp":"^[\x01\x02][\x01- ]\x06.*c\x82sc","http":"[\x09-\x0d -~]*"}
                
            return protocolos
            
    def enviarFila(self, routing_key, mensagem):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
               "", 5672, '/starwars', pika.PlainCredentials("skywalker", "luke")))
        channel = connection.channel()
        channel.exchange_declare(exchange='topic_logs',type='topic')
        channel.basic_publish(exchange='topic_logs',routing_key=routing_key,body=mensagem)
        
        print " [x] Sent %r:%r" % (routing_key, mensagem)
        
        connection.close()
    
    def iniciarColeta(self, file="", tempo = 60):
        print "Coletando..."
        protocolos = self.listarProtocolos()
        print protocolos
        contPkt = 0
        for ts, pkt in pcap.pcap(file):
            contPkt+=1
            eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
            protRede = ""
            protTransporte = ""
            protApp = ""
            
            ip = eth.data
            if isinstance(ip,dpkt.ip.IP):
                mensagem = "Rede: IP.Tamanho: "+str(len(pkt))+".Timestamp: "+str(ts)
                print mensagem
                #self.emit_topic("ip",mensagem)
                #self.emit_topic("all",mensagem)
                
                transp = ip.data
                if isinstance(transp,dpkt.tcp.TCP) or isinstance(transp,dpkt.udp.UDP):
                    if isinstance(transp,dpkt.tcp.TCP):
                        transporte = "TCP"
                    elif isinstance(transp,dpkt.udp.UDP):
                        transporte = "UDP"
                    
                    mensagem = "Transporte: "+transporte+".Rede: IP.Tamanho: "+str(len(pkt))+".Timestamp: "+str(ts)
                    print mensagem
                    #self.emit_topic(transporte,mensagem)
                    #self.emit_topic("all",mensagem)
                    
                    self.contProtocolos["all"] += 1
                    app = transp.data.lower()
                    found = False
                    for p in protocolos.items():
                        expressao = re.compile(p[1])
                        print "Capturada: " + str(expressao) + " | Original: " + str(p)
                        if expressao.search(app):
                            mensagem = "App: "+p[0]+".Transporte: "+transporte+".Rede: IP.Tamanho: "+str(len(pkt))+".Timestamp: "+str(ts)
                            print mensagem
                            #self.emit_topic(p[0],mensagem)
                            #self.emit_topic("all",mensagem)
                            self.contProtocolos[p[0]] += 1
                            found = True
        					
                        if (not found):
                            mensagem = "App: "+p[0]+".Transporte: "+transporte+".Rede: IP.Tamanho: "+str(len(pkt))+".Timestamp: "+str(ts)
                            print mensagem
                            #self.emit_topic("unknown",mensagem)
                            self.contProtocolos["unknown"] += 1
                else:
                    #self.logErros.writelines("#captura_pacotes: ", transp, " \n")
                    print 'erro'
            else:
                self.contProtocolos["nonIp"] += 1
        
        for p in self.contProtocolos.items():
        	print(p[0]+" Pkts:"+str(p[1]))

if __name__ == '__main__':
    
    various = Various()
    