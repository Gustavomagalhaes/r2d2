import socket, socketerror, sys, os, threading, time, traceback
from socketerror import *

class Monitor():

    def __init__(self):
        
        self.destino = ('<broadcast>', 6000)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #self.clientSocket.settimeout(20)
        self.statusComando = None
        self.coletores = {}
        self.coletorAtual = ""
        self.listadecomandos = {"LISTAR":"", "COLETAR":"", "SUSPENDER":"", "CONTINUAR":"", "DOWNLOAD":"", "SAIR":""}
        
        #socketerror
        #self.downloadSocket = socketError(socket.AF_INET, socket.SOCK_DGRAM)
        #self.downloadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.downloadSocket.settimeout(2.0)
        #self.downloadSocket.setErrorProb(0.5)
        self.file = None
        
        self.run()
        
    def getListaComandos(self):
        return self.listadecomandos
        
    def getColetores(self):
        return self.coletores
        
    def setColetor(self, coletor, status):
        self.coletores[(coletor)] = status
        
    def setColetorAtual(self, coletor):
        self.coletorAtual = coletor
        
    def getColetorAtual(self):
        return self.coletorAtual
    
    def getClientSocket(self):
        return self.clientSocket
        
    def getDestino(self):
        return self.destino
        
    def run(self):
        monitor = threading.Thread(target=self.receive)
        monitor.start()
        
    def receiveDownload(self):
        
        try:
            clientSocket = self.getClientSocket()
            string = []
            cont = 0
            while 1:
                print 'antes do receive'
                mensagem, endereco = clientSocket.recvfrom(8192)
                print mensagem
                if mensagem[0:3] == "ACK":
                    if mensagem[-10:] != "COM:THEEND":
                        string.append(mensagem[3:].replace("COM:THEEND", ""))
                        self.enviarComando("NACK"+str(cont), endereco)
                        cont += 1
                        continue
                    else:
                        string.append(mensagem[3:].replace("COM:THEEND", ""))
                        self.enviarComando("NACK"+str(cont), endereco)
            
            file = open("log_"+endereco[0]+".txt", "w")
            for line in string:
                file.write(line)
            file.close()
            print "Download realizado com sucesso."
            #self.downloadSocket.close()
        except:
            traceback.print_exc()
                    
            
    
    def receive(self):
        
        coletores = self.getColetores()
        clientSocket = self.getClientSocket()
        listadecomandos = self.getListaComandos()
        tComando = threading.Thread(target=self.inserirComando)
        
        while 1:
            clientSocket.sendto("MONITOR", self.getDestino())
            mensagem, endereco = clientSocket.recvfrom(2048)
            print mensagem
            if mensagem == "COLETOR":
                if endereco[0] not in coletores.keys():
                    self.setColetor(endereco[0], "[INATIVO]")
                
                if not coletores == True and self.statusComando == None:
                    tComando.start()
                    self.statusComando = True
                elif not coletores == False:# and self.statusComando == True:
                    continue
            elif mensagem[0:4] == "COM:":
                mensagem = mensagem[4:]
                if mensagem == "CAPTURANDO":
                    self.setColetor(endereco[0], "[COLETANDO]")
                elif mensagem == "SUSPENSO":
                    self.setColetor(endereco[0], "[SUSPENSO]")
                elif mensagem == "DOWNLOAD":
                    clientSocket.sendto("DOWNLOAD", (endereco[0],6321))
                    print 'mandou 2-DOWNLOAD'
                    self.receiveDownload()
                else:
                    continue
                self.inserirComando()
    
    def printCharacters(self):
        #os.system('clear')
        print "                                         "
        print "   (C3PO)                                "            
        print "         \  .-.                          "            
        print "           /_ _\                         "             
        print "           |o^o|                         "              
        print "           \ _ /                         "               
        print "          .-'-'-.                        "
        print "        /`)  .  (`\            (R2D2)    "
        print "       / /|.-'-.|\ \         /           "          
        print "       \ \| (_) |/ /  .-''-.             "          
        print "        \_\ -.- /_/  /[] _ _\            "          
        print "        /_/ \_/ \_\ _|_o_LII|_           "          
        print "          |'._.'|  / | ==== | \          "          
        print "          |  |  |  |_| ==== |_|          "          
        print "           \_|_/    ||' ||  ||           "          
        print "           |-|-|    ||LI  o ||           "          
        print "           |_|_|    ||'----'||           "          
        print "__________/_/_\_\__/__|____|__\__________"
        print "                                         "
    
    def ask(self):
        comando = raw_input("[R2D2] Insira um comando > ")
        return comando
    
    def stopPoing(self):
        comando = raw_input("> ")
        
    def listaDeColetores(self):
        self.printCharacters()
        print "Lista de coletores:\n"
        for coletor, status in self.getColetores().iteritems():
            print str(coletor) + ": " + status
            
    def suspenderColetores(self):
        self.printCharacters()
        self.listaDeColetores()
        print "\nEscolha o coletor que deseja suspender:\n"
        coletor = self.ask()
        self.enviarComando("SUSPENDER", coletor)
        
    def continuarColetando(self):
        self.printCharacters()
        self.listaDeColetores()
        print "\nEscolha o coletor que deseja continuar:\n"
        coletor = self.ask()
        self.enviarComando("CONTINUAR", coletor)
        
    def iniciarColeta(self):
        self.printCharacters()
        self.listaDeColetores()
        print "\nEscolha o coletor que deseja coletar:\n"
        coletor = self.ask()
        self.enviarComando("COLETAR", coletor)
        
    def downloadLog(self):
        self.printCharacters()
        self.listaDeColetores()
        print "\nEscolha o coletor que deseja fazer download:\n"
        coletor = self.ask()
        self.enviarComando("DOWNLOAD", coletor)
        
    def enviarComando(self, comando, coletor):
        clientSocket = self.getClientSocket()
        listadecomandos = self.getListaComandos()
        if comando not in listadecomandos.keys():
            self.inserirComando()
        else:
            try:
                if comando != "DOWNLOAD" and comando[0:4] != "NACK":
                    clientSocket.sendto(comando, (coletor, 6000))
                    self.receive()
                else:
                    #downloadSocket.sendWithError(comando)
                    clientSocket.sendto(comando, (coletor, 6000))
                    print 'enviou DOWNLOAD'
            except:
                traceback.print_exc()
                print "..."
    
    def inserirComando(self):
        while True:
            comando = ""
            listadecomandos = self.getListaComandos()
            while comando not in listadecomandos.keys():
                #os.system('clear')
                self.printCharacters()
                print ""
                print "| LISTAR | COLETAR | SUSPENDER | CONTINUAR | DOWNLOAD | SAIR |"
                print ""
                comando = self.ask().upper()
            if comando == "LISTAR":
                self.listaDeColetores()
                self.stopPoing()
            elif comando == "SUSPENDER":
                self.suspenderColetores()
            elif comando == "CONTINUAR":
                self.continuarColetando()
            elif comando == "COLETAR":
                self.iniciarColeta()
            elif comando == "DOWNLOAD":
                self.downloadLog()
            elif comando == "SAIR":
                os.system('clear')
                break
            else:
                self.enviarComando(comando, '')
                
if __name__ == '__main__':
    
    monitor = Monitor()
    #monitorThread = threading.Thread(target=monitor.start, args=())
    #monitorThread.start()
    #monitor.inserirComando()
