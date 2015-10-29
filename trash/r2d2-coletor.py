# -*- coding: cp1252 -*-
#PARA PARAR O PROCESSO PARALELO DO COLETOR USAR sudo pkill -f r2d2-coletor.py
import os
import socket, traceback, time, pcap, dpkt, re, pika, sys
from thread import *

class Coletor:
    
    def __init__(self, ip):
        self.tamanhoPacote = 1024
        self.hostBroadcast = ''
        self.portaEnvioBroadcast = 9000
        self.portaRecebeBroadcast = 9001
        self.ip = ip
        self.envioBroadcast = '<broadcast>'
        self.broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcastSocket.settimeout(10)
        self.status = True
        
    def abrirConexao(self):
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        while True:
            self.broadcastSocket.sendto("MONITOR", (self.envioBroadcast, self.portaRecebeBroadcast))
            print("Descobrindo...")
            
            try:
                message, serverAddress = self.broadcastSocket.recvfrom(2048)
                if str(message) == "APRESENTAR":
                    print("Monitor " + serverAddress[0] + " descoberto.")
                    print("Aguardando comando.")
                    self.broadcastSocket.close()
                    break
            except Exception:
                continue
            
    
    def receberComandoUnicast(self):
        try:
            self.broadcastSocket.bind(("", 9000))
        except:
            self.broadcastSocket.close()
            self.broadcastSocket.bind(("", 9000))
            
        
        while True:
            try:
                
                message, clientAddress = self.broadcastSocket.recvfrom(2048)
                if message == "PARAR":
                    self.status = False
                elif message == "CONTINUAR":
                    self.status = True
                    
                print("Ok")
                self.broadcastSocket.sendto("OK", clientAddress)
            except (KeyboardInterrupt, SystemExit):
                self.broadcastSocket.close()
                
            except:
                continue
            
    def emitMsg(self, routing_key, msg):
        credentials = pika.PlainCredentials('skywalker', 'luke')
        connection = pika.BlockingConnection(pika.ConnectionParameters(
               self.getIp(), 5672, '/starwars', credentials))
        channel = connection.channel()
        channel.exchange_declare(exchange='topic_logs',type='topic')
        channel.basic_publish(exchange='topic_logs',routing_key=routing_key,body=mensagemProtocolo)
        
        print " [x] Sent %r:%r" % (routing_key, mensagemProtocolo)
        
        connection.close()
        
    def getIp(self):
        return self.ip
    
    def setIp(self, ip):
        self.ip = ip
        
    
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
            protocolos = {"ssl":"^(.?.?\x16\x03.*\x16\x03|.?.?\x01\x03\x01?.*\x0b)", "ssh":"^ssh-[12]\.[0-9]", "ssdp":"^notify[\x09-\x0d ]\*[\x09-\x0d ]http/1\.1[\x09-\x0d -~]*ssdp:(alive|byebye)|^m-search[\x09-\x0d ]\*[\x09-\x0d ]http/1\.1[\x09-\x0d -~]*ssdp:discover", "bittorrent":"^(\x13bittorrent protocol|azver\x01$|get /scrape\?info_hash=)", "dhcp":"^[\x01\x02][\x01- ]\x06.*c\x82sc","http":"[\x09-\x0d -~]*"}
                
            return protocolos
            
    def iniciarColetor(self, file="", tempo = 60):
        cont = 0
        timeIni = time.time()
        protocolos = self.listarProtocolos()
        
        for ts, pkt in pcap.pcap(file):
            if self.status == True:
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
            else:
                time.sleep(1)

if __name__ == '__main__':
    
    print("C3PO: Coletor iniciado")
    
    c3po = Coletor("ip")
    c3po.abrirConexao()
    c3po.receberComandoUnicast()
    c3po.iniciarColetor("test.pcap",10000)