# -*- coding: utf-8 -*-
import os, socket, re, time, pcap, dpkt, threading
from threading import Thread

class Various(Thread):
    
    def __init__(self):
        self.status = None
        Thread.__init__(self)
        self.stopRequest = threading.Event()
        self.pauseRequest = threading.Event()
        self.pacotes = {}
        self.contProtocolos = self.contProtocolos = {"http":0, "ssdp":0, "ssl":0, "dhcp":0, "ssh":0, "unknown":0, "all":0, "nonIp":0}
        
        
    def getStatus(self):
        return self.status
        
    def setStatus(self, status):
        self.status = status
        
    def run(self):
        while not self.stopRequest.isSet():
            if not self.pauseRequest.isSet():
                self.iniciarColeta("test.pcap",10000)
            else:
                time.sleep(5)
        time.sleep(5)
        print "Yoda: Parado isto."
        
    def stop(self, timeout = None):
        self.stopRequest.set()
        super(Various, self).join(timeout)
        
    def pause(self, timeout = None):
        self.pauseRequest.set()

    def resume(self, timeout = None):
        self.pauseRequest.clear()
    
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
    
    def iniciarColeta(self, file="", tempo = 60):
        cont = 0
        timeIni = time.time()
        protocolos = self.listarProtocolos()
        
        for ts, pkt in pcap.pcap(file):
            if self.getStatus() == True:
                time.sleep(1)
                
                try:
                    cont += 1
                    timeAtual = time.time()
                    if timeAtual - timeIni > tempo:
                        break
                    
                    enl = dpkt.ethernet.Ethernet(pkt)
                    layerRede = "NA"
                    layerTrans = "NA"
                    layerApp = "NA"
                    print("Pacote " + cont + " da camada de enlace - Ethernet")
                    rede = enl.data
                    
                    #rede
                    if type(rede) != (""):
                        if (rede == dpkt.ip.IP):
                            layerRede = "IP"
                        elif (rede == dpkt.arp.ARP):
                            layerRede = "ARP"
                        else:
                            layerRede = "UNKNOWN"
                        msgRede = ("Rede: " + layerRede + " | Timestamp: " +str(ts)+ " Tamanho: " + str(len(pkt)))
                        #emitir(layerRede, msgRede)
                        trns = rede.data
                        
                        #transporte
                        if type(trns) != (""):
                            if (trns == dpkt.tcp.TCP):
                                layerTrans = "TCP"
                            elif (trns == dpkt.udp.UDP):
                                layerTrans = "UDP"
                            else:
                                layerTrans = "UNKNOWN"
                            msgTrans = ("Transporte: " + layerTrans+ " | Rede: " + layerRede + " | Timestamp: " +str(ts)+ " Tamanho: " + str(len(pkt)))
                            #emitir(layerTrans, msgTrans)
                            app = trns.data.lower()
                            found = False
                            
                            #aplicação
                            for p in protocolos.items():
                                expressao = re.compile(p[1])
                                if expressao.search(app):
                                    msgTrans = ("Aplicação: " + p[0] + " | Transporte: " + layerTrans+ " | Rede: " + layerRede + " | Timestamp: " +str(ts)+ " Tamanho: " + str(len(pkt)))
                                    #emitir(layerApp, msgApp)
                                    found = True
                					
                                if (not found):
                                    msgTrans = ("Aplicação: " + str(app) + " | Transporte: " + layerTrans+ " | Rede: " + layerRede + " | Timestamp: " +str(ts)+ " Tamanho: " + str(len(pkt)))
                    
                    msg = "Aplicação: " + str(app) + " | Transporte: " + layerTrans+ " | Rede: " + layerRede + " | Timestamp: " +str(ts)+ " Tamanho: " + str(len(pkt))
                    print msg
                    #emititr
                
                except:
                    print""
            elif self.getStatus() == False:
                self.pause()
                while self.getStatus() == False:
                    time.sleep(3)
                self.resume()
            else:
                time.sleep(1)
    
    