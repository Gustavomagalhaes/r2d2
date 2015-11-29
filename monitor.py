import socket, sys, os, threading, time, traceback, time

class Monitor():

    def __init__(self):
        
        self.destino = ('<broadcast>', 6000)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.clientSocket.settimeout(20)
        self.coletores = {}
        self.coletorAtual = ""
        self.listadecomandos = {"LISTAR":"", "COLETAR":"", "SUSPENDER":"", "CONTINUAR":"", "SAIR":""}
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
        monitor = threading.Thread(target=self.iniciarMonitor)
        monitor.start()
        
    def iniciarMonitor(self):
        # Inicia o monitor para que esse seja percebido pelos coletores
        clientSocket = self.getClientSocket()
        coletores = self.getColetores()
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        comandoStatus = False
        
        while 1:
            comando = threading.Thread(target=self.inserirComando)
            #PRIMEIRO ENVIO
            clientSocket.sendto("MONITOR", self.getDestino())
            #PRIMEIRO RECEIVE
            mensagem, endereco = clientSocket.recvfrom(2048)
            if mensagem != "COLETOR":
                break
            else:
                print "[R2D2] Coletor %s localizado: %s" % (str(endereco), mensagem)
                if endereco[0] not in coletores.keys():
                    self.setColetor(endereco[0], "[INATIVO]")
                    #print "[R2D2] Coletor adicionado a lista de coletores."
                    #self.getClientSocket().close()
                if comandoStatus == False:
                    comando.start()
                    comandoStatus = True
                else:
                    continue
    
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
        
    def enviarComando(self, comando, coletor):
        clientSocket = self.getClientSocket()
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        while 1:
            try:
                #SEGUNDO ENVIO
                clientSocket.sendto(comando, (coletor, 6000))
                print 'enviou'
                #SEGUNDO RECEIVE
                time.sleep(3)
                mensagem, endereco = clientSocket.recvfrom(2048)
                print mensagem
                if mensagem == "CAPTURANDO":
                    self.setColetor(endereco[0], "[COLETANDO]")
                elif mensagem == "SUSPENSO":
                    self.setColetor(endereco[0], "[SUSPENSO]")
                    
                break
            except:
                traceback.print_exc()
                print "excepto"

    def inserirComando(self):
        while True:
            comando = ""
            listadecomandos = self.getListaComandos()
            while comando not in listadecomandos.keys():
                #os.system('clear')
                self.printCharacters()
                print ""
                print "| LISTAR | COLETAR | SUSPENDER | CONTINUAR | SAIR |"
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
