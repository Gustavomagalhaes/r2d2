# -*- coding: cp1252 -*-
#PARA PARAR O PROCESSO PARALELO DO COLETOR USAR sudo pkill -f coletor.py
import os, socket, traceback, sys, threading, re, time, pcap, dpkt, pika, logging
#logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

class Coletor():
    
    def __init__(self):
        
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.settimeout(20)
        
        #coleta
        self.statusColeta = None
        self.pacotes = {}
        self.contProtocolos = {"http":0, "ssdp":0, "ssl":0, "dhcp":0, "ssh":0, "nbns":0, "dropbox":0, "unknown":0, "bittorrent":0, "all":0, "nonIp":0}
        
        c3po = threading.Thread(target=self.localizarMonitor)
        c3po.start()
        
        #self.localizarMonitor()
        
    def getServerSocket(self):
        return self.serverSocket
    
    def getPacotes(self):
        return self.pacotes
        
    def setPacote(self, chave, conteudo):
        self.pacotes[(chave)] = conteudo
        
    def getStatusColeta(self):
        return self.statusColeta
        
    def setStatusColeta(self, thread, statusColeta):
        self.statusColeta = statusColeta
        if self.statusColeta == "False" and statusColeta == "True":
            thread.start()
        elif self.statusColeta == "True" and statusColeta == "False":
            thread.stop()
            
        
    def getcontProtocolos(self):
        return self.contProtocolos

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
                raise
            except:
                traceback.print_exc()
                #print "[C3PO] Ainda procurando monitor..."
        serverSocket.close()
    
    def receberComando(self, monitor):
        
        yoda = threading.Thread(target=self.iniciarColeta("files/gus.pcap",0))
        # yoda = threading.Thread(target=self.iniciarColeta("",0))
        serverSocket = self.getServerSocket()
        
        print "[C3PO] Aguardando comando do monitor..."
    
        while 1:
            try:
                
                mensagem, endereco = self.serverSocket.recvfrom(8192)
                print mensagem
                print endereco
                if mensagem == "COLETAR" and self.getStatusColeta() == None:
                    self.serverSocket.sendto("CAPTURANDO", endereco)
                    self.setStatusColeta(yoda, True)
                    print "[C3PO] Capturando"
                    yoda.start()
                    
                elif mensagem == "COLETAR" and self.getStatusColeta() == False:
                    self.serverSocket.sendto("CAPTURANDO", endereco)
                    print "[C3PO] Capturando"
                    self.setStatusColeta(yoda, True)
                    
                elif mensagem == "SUSPENDER" and self.getStatusColeta() == True:
                    self.serverSocket.sendto("SUSPENSO", endereco)
                    print "[C3PO] Suspenso"
                    self.setStatusColeta(yoda, False)
                    # yoda.OnStop()
                  #  yoda.setStatus(False)
                    
                elif mensagem == "CONTINUAR" and self.getStatusColeta() == False:
                    self.serverSocket.sendto("CAPTURANDO", endereco)
                    print "[C3PO] Capturando"
                    self.setStatusColeta(yoda, True)
                  #  yoda.setStatus(True)
                 
                elif mensagem == "MONITOR":
                    continue
                    
                    
                self.receberComando(monitor)
                
                #self.serverSocket.sendto("OK", endereco)
            #except (KeyboardInterrupt, SystemExit):
              #  yoda.stop()
              #  raise
            except:
                traceback.print_exc()
                print "excepto"
        
    
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
            inicio = time.time()
            contPkt+=1
            eth = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
            protRede = ""
            protTransporte = ""
            protApp = ""
            print self.getStatusColeta()
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
                    found = False
                    for p in protocolos.items():
                        expressao = re.compile(p[1])
                        if expressao.search(app):
                            duracao = time.time() - inicio
                            mensagem = p[0]+"#"+transporte+"#IP#"+str(len(pkt))+"#"+str(ts)+"#"+str(duracao)+"#"+str((len(pkt)/duracao))
                            # mensagem = p[0]+"#"+transporte+"#IP#"+str(len(pkt))+"#"+str(ts)
                            #print mensagem
                            # HTTP entre outros. 
                            if (self.getStatusColeta() == True):
                                self.enviarFila(p[0],mensagem)
                                self.enviarFila("all",mensagem)
                            self.contProtocolos[p[0]] += 1
                            found = True
        					
                        if (not found):
                            duracao = time.time() - inicio
                            mensagem = "UNKOWN#"+transporte+"#IP#"+str(len(pkt))+"#"+str(ts)+"#"+str(duracao)+"#"+str((len(pkt)/duracao))
                            # mensagem = "UNKOWN#"+transporte+"#IP#"+str(len(pkt))+"#"+str(ts)
                            #print mensagem
                            if (self.getStatusColeta() == True):
                                self.enviarFila("unknown",mensagem)
                                self.contProtocolos["unknown"] += 1
                else:
                    #self.logErros.writelines("#captura_pacotes: ", transp, " \n")
                    print 'log'
            else:
                self.contProtocolos["nonIp"] += 1
        
        #for p in self.contProtocolos.items():
        #	print(p[0]+" Pkts:"+str(p[1]))
        
    def enviarFila(self, routing_key, mensagem):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
               "", 5672, '/starwars', pika.PlainCredentials("skywalker", "luke")))
        channel = connection.channel()
        channel.exchange_declare(exchange='topic_logs',type='topic')
        channel.basic_publish(exchange='topic_logs',routing_key=routing_key,body=mensagem)
        
        print "SENT TO [%s]: %r" % (routing_key.upper(), mensagem)
        
        connection.close()

if __name__ == '__main__':
    os.system('clear')
    coletor = Coletor()
    #coletorThread = threading.Thread(target=coletor.start)
    #coletorThread.start()
    #comandoThread = threading.Thread(target=coletor.run, args=())