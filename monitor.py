import socket, sys, os

class Monitor:

    def __init__(self):
        
        self.destino = ('<broadcast>', 5000)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.clientSocket.settimeout(20)
        self.coletores = {}
        self.coletorAtual = ""
        
        self.iniciarMonitor()
        
    def getColetores(self):
        return self.coletores
        
    def setColetor(self, coletor):
        self.coletores[(coletor)] = "Coletando"
        
    def setColetorAtual(self, coletor):
        self.coletorAtual = coletor
        
    def getColetorAtual(self):
        return self.coletorAtual
    
    def getClientSocket(self):
        return self.clientSocket
        
    def getDestino(self):
        return self.destino
    
    def iniciarMonitor(self):
        
        clientSocket = self.getClientSocket()
        coletores = self.getColetores()
        
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        clientSocket.sendto("MONITOR", self.getDestino())
        
        print "R2D2: Aguardando respostas; pressione 'Ctrl+C' para parar."
        
        # while 1:
        #     mensagem, endereco = clientSocket.recvfrom(2048)
        #     if not len(mensagem):
        #         break
        #     print "R2D2: Coletor %s localizado: %s" % (str(endereco), mensagem)
        #     if endereco[0] not in coletores.keys():
        #         self.setColetor(endereco[0])
        #         print "R2D2: Coletor adicionado a lista de coletores."
        #     #self.getClientSocket().close()
        #     break
    
    def printCharacters(self):
        print "                                     "
        print "   (C3PO)                            "            
        print "         \  .-.                      "            
        print "           /_ _\                     "             
        print "           |o^o|                     "              
        print "           \ _ /                     "               
        print "          .-'-'-.                    "
        print "        /`)  .  (`\            (R2D2)"
        print "       / /|.-'-.|\ \         /       "          
        print "       \ \| (_) |/ /  .-''-.         "          
        print "        \_\ -.- /_/  /[] _ _\        "          
        print "        /_/ \_/ \_\ _|_o_LII|_       "          
        print "          |'._.'|  / | ==== | \      "          
        print "          |  |  |  |_| ==== |_|      "          
        print "           \_|_/    ||' ||  ||       "          
        print "           |-|-|    ||LI  o ||       "          
        print "           |_|_|    ||'----'||       "          
        print "          /_/ \_\  /__|    |__\      "  
    
    def ask(self):
        comando = raw_input("R2D2: Insira um comando >")
        return comando
        
    def listarColetores(self):
        os.system('clear')
        print "Lista de coletores:\n"
        for coletor, status in self.getColetores().iteritems():
            print str(coletor) + ": " + status
            
        comando = self.ask()
    
    def suspenderColetores(self):
        os.system('clear')
        self.listarColetores()
        print "Escolha o coletor que deseja suspender:\n"
        comando = self.ask()
        
    def continuarColetando(self):
        os.system('clear')
        print "CONTINUANDO"
        comando = self.ask()
        
    def iniciarColeta(self):
        os.system('clear')
        print "COLETANDO"
        comando = self.ask()
        
    def enviarComando(self, comando):
        self.listarColetores()
        if self.getColetorAtual() == "":
            self.setColetorAtual(raw_input("Insira o IP de um coletor valido:"))
        
        self.getClientSocket().setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mensagem = ""
        while mensagem != "OK":
            print "Aguardando..."
            try:
                print "entrou no try"
                print self.getColetorAtual()
                self.getClientSocket().sendto(comando, (self.getColetorAtual(), 5000))
                self.setColetorAtual("")
                mensagem, endereco = self.getClientSocket().recvfrom(2048)
                break
            
            except:
                print "..."
                continue
    
    def inserirComando(self):
        while True:
            comando = ""
            listadecomandos = {"LISTAR":"", "COLETAR":"", "SUSPENDER":"", "CONTINUAR":""}
            while comando not in listadecomandos.keys():
                os.system('clear')
                self.printCharacters()
                print ""
                print "| LISTAR | COLETAR | SUSPENDER | CONTINUAR |"
                print ""
                comando = self.ask().upper()
            if comando == "LISTAR":
                self.listarColetores()
            elif comando == "SUSPENDER":
                self.suspenderColetores()
            elif comando == "CONTINUAR":
                self.continuarColetando()
            elif comando == "COLETAR":
                self.iniciarColeta()
            else:
                self.enviarComando(comando)
                
            
            
        
if __name__ == '__main__':
    
    monitor = Monitor()
    monitor.inserirComando()