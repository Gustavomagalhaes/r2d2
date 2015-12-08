# -*- coding: cp1252 -*-
#PARA PARAR O PROCESSO PARALELO DO COLETOR USAR sudo pkill -f coletor.py
import os, socket, socketerror, traceback, sys, threading, re, time, pcap, dpkt, pika, logging, datetime
#logging.basicConfig(filename='erros.log',level=logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

class Coletor():
    
    def __init__(self, ip):
        
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.downloadSocket = socketerror.socketError(socket.AF_INET, socket.SOCK_DGRAM)
        
        
        #socketerror
        self.downloadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.settimeout(20)
        self.logFile = "log.txt"
        self.file = None
        
        #coleta
        self.statusColeta = None
        self.pacotes = {}
        self.contProtocolos = {"unknown":0, "all":0, "nonIp":0}
        self.fluxos = {}
        
        #rabbit
        self.ip = ip
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.getIp(), 5672, '/starwars', pika.PlainCredentials("skywalker", "luke")))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='topic_logs', type='topic')
        
        c3po = threading.Thread(target=self.localizarMonitor)
        c3po.start()
        
        leia = threading.Thread(target=self.downloadLog)
        leia.start()
        
        #self.localizarMonitor()
        
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
        self.downloadSocket.bind(("",6020))
        while 1:
            print "Aguardando download"
            mensagem, endereco, = self.downloadSocket.recvWithError(8192)
            
            if mensagem == "DOWNLOAD":
                temp = self.file.read()
                self.closeLog()
                buffers = {}
                
                for i in range(0, (len(temp)/256)):
                    buffers["ACK"+str(i)] = temp[i*256:((i+1)*256)]
                
                for index in range(0, len(buffers.keys())):
                    ACK = "ACK"+str(index)
                    content = buffers[ACK]
                    content = content.replace("\n", "\n ")
                    self.downloadSocket().settimeout(5)
                    while not ("NACK"+str(index)) in mensagem:
                        try:
                            if index == len(buffers.keys()) -1:
                                self.downloadSocket.sendWithError(ACK+content+"COM:THEEND", endereco)
                                mensagem, endereco = self.downloadSocket.recvWithError(8192)
                            else:
                                self.downloadSocket.sendWithError(ACK+content, endereco)
                                mesnage, endereco = self.downloadSocket.recvWithError(8192)
                        except:
                            print "Timeout"
                

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
                    #print "[C3PO] Aguardando..."
                    comando = threading.Thread(target=self.receberComando(endereco))
                    comando.start()
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
        
    def receberComando(self, monitor):
        
        if self.getStatusColeta() == True:
            yoda = threading.Thread(target=self.iniciarColeta("files/gus.pcap",0))
        # yoda = threading.Thread(target=self.iniciarColeta("",0))
        serverSocket = self.getServerSocket()
        
        print "\n[C3PO] Aguardando comando do monitor..."
    
        while 1:
            try:
                
                mensagem, endereco = self.serverSocket.recvfrom(8192)
                # print mensagem
                # print endereco
                if mensagem == "COLETAR": 
                    self.serverSocket.sendto("COM:CAPTURANDO", endereco)
                    self.setStatusColeta(True)
                    print "[C3PO] Capturando"

                elif mensagem == "SUSPENDER" and self.getStatusColeta() != False:
                    self.serverSocket.sendto("COM:SUSPENSO", endereco)
                    print "[C3PO] Suspenso"
                    self.setStatusColeta(False)
                    # yoda.OnStop()
                  #  yoda.setStatus(False)
                    
                elif mensagem == "CONTINUAR":
                    self.serverSocket.sendto("COM:CAPTURANDO", endereco)
                    print "[C3PO] Capturando"
                    self.setStatusColeta(True)
                  #  yoda.setStatus(True)
                 
                elif mensagem == "MONITOR":
                    continue
                    
                    
                self.receberComando(monitor)
                
                #self.serverSocket.sendto("OK", endereco)
            #except (KeyboardInterrupt, SystemExit):
              #  yoda.stop()
              #  raise
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
                                
                #protocolos[chave] = re.compile(valor)
                #valor = re.compile(valor)
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
            #protocolos = {"ssl":"^(.?.?\x16\x03.*\x16\x03|.?.?\x01\x03\x01?.*\x0b)", "ssh":"^ssh-[12]\.[0-9]", "ssdp":"^notify[\x09-\x0d ]\*[\x09-\x0d ]http/1\.1[\x09-\x0d -~]*ssdp:(alive|byebye)|^m-search[\x09-\x0d ]\*[\x09-\x0d ]http/1\.1[\x09-\x0d -~]*ssdp:discover", "bittorrent":"^(\x13bittorrent protocol|azver\x01$|get /scrape\?info_hash=)", "dhcp":"^[\x01\x02][\x01- ]\x06.*c\x82sc", "http":"[\x09-\x0d -~]*"}
                
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
                    duracao = time.time() - inicio
                    
                    mensagem = "##IP#"+str(len(pkt))+"#"+str(ts)+"#"+str(duracao)+"#"+str((len(pkt)/duracao)) 
                    
                    
                    # mensagem = "##IP#"+str(len(pkt))+"#"+str(ts)
                    # print mensagem
                    # print self.getStatusColeta()
                    
                    # Nao tem fila IP
                    # if (self.getStatusColeta() == True):
                        # self.enviarFila("ip",mensagem)
                        # self.enviarFila("all",mensagem)
                    
                    transp = ip.data
                    if isinstance(transp,dpkt.tcp.TCP) or isinstance(transp,dpkt.udp.UDP):
                        if isinstance(transp,dpkt.tcp.TCP):
                            transporte = "TCP"
                        elif isinstance(transp,dpkt.udp.UDP):
                            transporte = "UDP"
                        
                        duracao = time.time() - inicio
                        mensagem = "#"+transporte+"#IP#"+str(len(pkt))+"#"+str(ts)+"#"+str(duracao)+"#"+str((len(pkt)/duracao))
                        # mensagem = "#"+transporte+"#IP#"+str(len(pkt))+"#"+str(ts)
                        #print mensagem
                        # Nao tem fila UDP
                        # if (self.getStatusColeta() == True):
                        #     self.enviarFila(transporte,mensagem)
                        #     self.enviarFila("all",mensagem)
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
                        
                        found = False
                        
                        if chaveFluxo not in self.fluxos.keys():
                            tamanho = len(app)
                            duracao = 0.000001
                            stormtrooper = threading.Thread(target=self.enviarFila(chaveFluxo))
                            self.fluxos[chaveFluxo] = [self.classificarProtocolo(app), ts, tamanho, duracao, stormtrooper, ts, 0, 1]
                            stormtrooper.start()
                        else:
                            self.fluxos[chaveFluxo][2] += len(app)
                            self.fluxos[chaveFluxo][6] = (ts - (self.fluxos[chaveFluxo][5] + self.fluxos[chaveFluxo][6]))
                            self.fluxos[chaveFluxo][7] += 1
                            self.fluxos[chaveFluxo][5] = ts
                            self.fluxos[chaveFluxo][3] = duracao + (ts - self.fluxos[chaveFluxo][1])
                            stormtrooper = threading.Thread(target=self.enviarFila(chaveFluxo))
                            stormtrooper.start()
                            self.fluxos[chaveFluxo][4] = stormtrooper
                        
                    else:
                        #self.logErros.writelines("#captura_pacotes: ", transp, " \n")
                        #print 'log'
                        self.openLog()
                        self.file.write("Erro na camada " + transp + " em " + str(time.time()) + "\n")            
                        self.closeLog()
                else:
                    self.contProtocolos["nonIp"] += 1
            
            except:
                self.openLog()
                self.file.write("Erro no pacote " + str(contPkt) + " em " + str(time.time()) + "\n")            
                self.closeLog()
            
        #for p in self.contProtocolos.items():
        #	print(p[0]+" Pkts:"+str(p[1]))
        
    def enviarFila(self, chaveFluxo):
        fluxo = self.fluxos[chaveFluxo]
        tamanho = fluxo[2]
        duracao = fluxo[3]
        quantidade = fluxo[7]
        routing_key = fluxo[0]
        
        if (quantidade > 1) and (tamanho > 0) and (duracao > 0.0000001):
            media = float(tamanho)/duracao
            atraso = float(fluxo[6])/quantidade
            mensagem = str(tamanho)+"#"+str(duracao)+"#"+str(media)+"#"+str(atraso)
            print "Fluxo " + str(chaveFluxo) + " sendo enviado..."
            self.channel.basic_publish(exchange='topic_logs',routing_key=routing_key,body=mensagem)
            self.channel.basic_publish(exchange='topic_logs',routing_key="ALL",body=mensagem)
        
            print "SENT TO [%s]: %r" % (routing_key.upper(), mensagem)

if __name__ == '__main__':
    os.system('clear')
    coletor = Coletor("192.168.25.117")
    #coletorThread = threading.Thread(target=coletor.start)
    #coletorThread.start()
    #comandoThread = threading.Thread(target=coletor.run, args=())