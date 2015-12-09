# -*- coding: cp1252 -*-
#PARA PARAR O PROCESSO PARALELO DO COLETOR USAR sudo pkill -f coletor.py
import os, socket, traceback, sys, threading, re, time, pcap, dpkt, pika, logging, datetime, sched
from socketerror import *
#logging.basicConfig(filename='erros.log',level=logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

class Coletor():
    
    def __init__(self, ip):
        
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.settimeout(20)
        
        #socketerror
        self.downloadSocket = socketError(socket.AF_INET, socket.SOCK_DGRAM)
        self.downloadSocket.settimeout(20)
        self.logFile = "log.txt"
        self.file = None
        
        
        #coleta
        self.statusColeta = None
        self.pacotes = {}
        self.contProtocolos = {"unknown":0, "all":0, "nonIp":0}
        self.fluxos = {}
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.startSchedule = False
        
        #rabbit
        self.ip = ip
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.getIp(), 5672, '/starwars', pika.PlainCredentials("skywalker", "luke")))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='topic_logs', type='topic')
        
        c3po = threading.Thread(target=self.localizarMonitor)
        c3po.start()

    def run(self):
        while True:
            self.schedule.run()
        
    def getIp(self):
        return self.ip
    
    def setIp(self, ip):
        self.ip = ip
        
    def getServerSocket(self):
        return self.serverSocket
    
    def getPacotes(self):
        return self.pacotes
        
    def setPacote(self, chave, conteudo):
        self.pacotes[(chave)] = conteudo
        
    def getStatusColeta(self):
        return self.statusColeta
        
    def setStatusColeta(self, statusColeta):
        self.statusColeta = statusColeta
            
        
    def getcontProtocolos(self):
        return self.contProtocolos
    
    def openLog(self, comando = "a"):
        self.file = open(self.logFile, comando)
        
    def closeLog(self):
        self.file.close()
        
    def downloadLog(self):
        print 'Download concluido'
        # while True:
        #     print "Aguardando download"
        #     self.downloadSocket.settimeout(None)
        #     mensagem, endereco = self.downloadSocket.recvWithError(8192)
            
        #     if mensagem == "DOWNLOAD":
        #         print "Msg DOWNLOAD recebida"
        #         self.openLog("r")
        #         print "Abriu log"
        #         temp = self.file.read()
        #         print "Leu log"
        #         self.closeLog()
        #         print "fechou log"
        #         buffers = {}
                
        #         try:
        #             print "entrou no try"
        #             print str(temp)
        #             for i in range(0, (len(temp)/256)):
        #                 print "Entrou no for i"
        #                 buffers["ACK"+str(i)] = temp[i*256:((i+1)*256)]
        #                 print "Adicionado " + "ACK"+str(i) + temp[i*256:((i+1)*256)] + "aos buffers"
                    
        #             for index in range(0, len(buffers.keys())):
        #                 print "entrou no for index"
        #                 ACK = "ACK"+str(index)
        #                 print "ACK: " + ACK
        #                 content = buffers[ACK]
        #                 content = content.replace("\n", "\n ")
        #                 print "CONTENT: " + content
        #                 self.downloadSocket.settimeout(None)
        #                 while not ("NACK"+str(index)) in mensagem:
        #                     try:
        #                         if index == len(buffers.keys()) -1:
        #                             self.downloadSocket.sendWithError(ACK+content+"COM:THEEND", endereco)
        #                             print "Pacote final " + ACK+content+"COM:THEEND" + " para " + str(endereco)
        #                             mensagem, endereco = self.downloadSocket.recvWithError(8192)
        #                         else:
        #                             self.downloadSocket.sendWithError(ACK+content, endereco)
        #                             print mensagem
        #                             print "Enviou " + ACK+content + " para " + str(endereco)
        #                             mensagem, endereco = self.downloadSocket.recvWithError(8192)
        #                     except:
        #                         traceback.print_exc()
        #                         print "Timeout"
        #         except:
        #             traceback.print_exc()
        #             print "caiu no except"
                

    def localizarMonitor(self, mensagem = "", endereco = ()):
        serverSocket = self.getServerSocket()
        
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        serverSocket.bind(('', 6000))
        
        print "[C3PO] Procurando monitor..."
    
        while 1:
            try:
                mensagem, endereco = serverSocket.recvfrom(8192)
                
                if mensagem == "MONITOR":
                    print "[C3PO] Monitor %s localizado" % (str(endereco))
                    serverSocket.sendto("COLETOR", endereco)
                    serverSocket.settimeout(None)
                    comando = threading.Thread(target=self.receberComando(endereco))
                    comando.start()
                    download = threading.Thread(target=self.enviarDownload(endereco))
                    download.start()
                    
                    break
                else:
                    continue
            except (KeyboardInterrupt, SystemExit):
                self.openLog()
                self.file.write("Localizar monitor: Operacao cancelada pelo usuario\n")            
                self.closeLog()
                
                raise
            except:
                self.openLog()
                self.file.write("Localizar monitor: Monitor nao localizado\n")            
                self.closeLog()
                
        serverSocket.close()
        
    def enviarDownload(self, monitor):
        downloadSocket = self.downloadSocket
        downloadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        downloadSocket.bind(('', 6321))
        downloadSocket.connect(monitor)
        
        print "\n[C3PO] Aguardando download do monitor..."
        
        while 1:
            try:
                
                mensagem, endereco = downloadSocket.recvWithError(8192)
                if mensagem == "DOWNLOAD":
                    print "[C3PO] Download"

                self.openLog("r")
                temp = self.file.read()
                self.closeLog()
                buffers = {}
                    
                for i in range(0, (len(temp)/256)):
                    buffers["ACK" + str(i)] = temp[i + 256 : ((i + 1) * 256)]
                
                for index in range(0, len(buffers.keys())):
                    print index
                    ACK = "ACK" + str(index)
                    content = buffers[ACK]
                    content = content.replace("\n", "\n ")
                if not ("NACK" + str(index)) in mensagem:
                    if index == len(buffers.keys())-1:
                        self.downloadSocket.sendWithError(ACK + content + "COM:THEEND", endereco)
                        break
                    else:
                        self.downloadSocket.sendWithError(ACK + content, endereco)
                        continue
                    
                    
                else:
                    continue
            except:
                self.openLog()
                self.file.write("Nenhuma resposta do download em " + str(time.time()) + "\n")            
                self.closeLog()
                
        downloadSocket.close()
        
    def receberComando(self, monitor):
        
        if self.getStatusColeta() == True:
            yoda = threading.Thread(target=self.iniciarColeta("files/test.pcap",0))
        serverSocket = self.getServerSocket()
        
        print "\n[C3PO] Aguardando comando do monitor..."
    
        while 1:
            try:
                
                mensagem, endereco = self.serverSocket.recvfrom(8192)
                if mensagem == "COLETAR": 
                    self.serverSocket.sendto("COM:CAPTURANDO", endereco)
                    self.setStatusColeta(True)
                    print "[C3PO] Capturando"

                elif mensagem == "SUSPENDER" and self.getStatusColeta() != False:
                    self.serverSocket.sendto("COM:SUSPENSO", endereco)
                    print "[C3PO] Suspenso"
                    self.setStatusColeta(False)
                    
                elif mensagem == "CONTINUAR":
                    self.serverSocket.sendto("COM:CAPTURANDO", endereco)
                    print "[C3PO] Capturando"
                    self.setStatusColeta(True)
                 
                elif mensagem == "MONITOR":
                    continue
                    
                    
                self.receberComando(monitor)
            except:
                self.openLog()
                self.file.write("Aguardando comando: sem comunicacao com o monitor em " + str(time.time()) + "\n")            
                self.closeLog()
                #print "except"
        
    
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
                                
                proto = {}
                arq = open("protocolos.txt","r")
                listaLinhas = arq.readlines()
                for linha in listaLinhas:
                    linha = linha.split(":")
                    expr = linha[1].replace("\n","")
                    nome= linha[0]
                    proto[nome] = expr
                protocolos[chave] = valor
                self.contProtocolos[chave] = 0
                
            return proto
    
    def classificarProtocolo(self, protocolo):
        for nome, p in self.listarProtocolos().iteritems():
            p = re.compile(p)
            if p.search(protocolo):            
                return nome
        return "unknown"
    
    def iniciarColeta(self, file="", tempo = 100):
        protocolos = self.listarProtocolos()
        contPkt = 0
        for ts, pkt in pcap.pcap(file):
            try:
                inicio = time.time()
                contPkt+=1
                eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
                protRede = ""
                protTransporte = ""
                protApp = ""
                ip = eth.data
                if isinstance(ip,dpkt.ip.IP) and (self.getStatusColeta() != None):
                    transp = ip.data
                    if isinstance(transp,dpkt.tcp.TCP) or isinstance(transp,dpkt.udp.UDP):
                        if isinstance(transp,dpkt.tcp.TCP):
                            transporte = "TCP"
                        elif isinstance(transp,dpkt.udp.UDP):
                            transporte = "UDP"
                        self.contProtocolos["all"] += 1
                        app = transp.data.lower()
                        
                        try:
                            ipOrigem = socket.inet_ntoa(ip.src)
                        except:                                
                            try:
                                ipOrigem = socket.inet_aton(ip.src.decode('utf-8'))
                            except:
                                ipOrigem = ip.src
                        
                        try:
                            ipDestino = socket.inet_ntoa(ip.dst)
                            
                        except:
                            try:
                                ipDestino = socket.inet_aton(ip.dst.decode('utf-8'))
                            except:
                                ipDestino = ip.dst

                        try:    
                            portaOrigem = transp.sport
                            portaDestino = transp.dport
                        except:
                            break
                        
                        chaveFluxo = (transporte, ipOrigem, portaOrigem, ipDestino, portaDestino)
                        #print str(chaveFluxo)
                        
                        found = False

                        if chaveFluxo not in self.fluxos.keys():
                            #print "A chave nao existe"
                            tamanho = len(app)
                            duracao = 0.000001
                            stormtrooper = self.schedule.enter(100, 1, self.enviarFila, argument=(chaveFluxo,))
                            self.startSchedule = True
                            self.fluxos[chaveFluxo] = [self.classificarProtocolo(app), ts, tamanho, duracao, stormtrooper, ts, 0, 1]
                            #print "Criou " + str(chaveFluxo)
                            self.enviarFila(chaveFluxo)
                            #print "Criou - Startou a thread"
                        else:
                            #print "A chave existe"
                            self.fluxos[chaveFluxo][2] += len(app)
                            stormtrooper = self.fluxos[chaveFluxo][4]
                            self.fluxos[chaveFluxo][6] = (ts - (self.fluxos[chaveFluxo][5] + self.fluxos[chaveFluxo][6]))
                            self.fluxos[chaveFluxo][7] += 1
                            self.fluxos[chaveFluxo][5] = ts
                            self.schedule.cancel(stormtrooper)
                            self.fluxos[chaveFluxo][3] = duracao + (ts - self.fluxos[chaveFluxo][1])
                            stormtrooper = self.schedule.enter(100, 1, self.enviarFila, argument=(chaveFluxo,))
                            self.startSchedule = True
                            #print "Atualizou " + str(self.fluxos.get(chaveFluxo))
                            self.enviarFila(chaveFluxo)
                            #print "Atualizou - Startou a thread"
                            self.fluxos[chaveFluxo][4] = stormtrooper
                        
                    else:
                        self.openLog()
                        self.file.write("Erro na camada " + transp + " em " + str(time.time()) + "\n")            
                        self.closeLog()
                else:
                    self.contProtocolos["nonIp"] += 1
            
            except:
                traceback.print_exc()
                self.openLog()
                self.file.write("Erro no pacote " + str(contPkt) + " em " + str(time.time()) + "\n")            
                self.closeLog()

    def enviarFila(self, chaveFluxo):
        #print "foi pra fila"
        fluxo = self.fluxos[chaveFluxo]
        tamanho = fluxo[2]
        duracao = fluxo[3]
        quantidade = fluxo[7]
        routing_key = fluxo[0]

        if (quantidade > 0) and (tamanho > 0):
            media = float(tamanho)/duracao
            #print media
            atraso = float(fluxo[6])/quantidade
            #print atraso
            mensagem = str(tamanho)+"|"+str(duracao)+"|"+str(media)#+"|"+str(atraso)
            #print mensagem
            print "Fluxo " + str(chaveFluxo) + " sendo enviado..."
            self.channel.basic_publish(exchange='topic_logs',routing_key=routing_key,body=mensagem)
            self.channel.basic_publish(exchange='topic_logs',routing_key="ALL",body=mensagem)
        
            print "SENT TO [%s]: %r" % (routing_key.upper(), mensagem)

if __name__ == '__main__':
    os.system('clear')
    ip = sys.argv[1]
    if not ip:
        ip = "192.168.25.118"
    coletor = Coletor(ip)