import socket, sys

class Monitor:

    def __init__(self):
        
        self.destino = ('<broadcast>', 5000)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
        
        while 1:
            mensagem, endereco = clientSocket.recvfrom(2048)
            if not len(mensagem):
                break
            print "R2D2: Coletor %s localizado: %s" % (str(endereco), mensagem)
            if endereco[0] not in coletores.keys():
                self.setColetor(endereco[0])
                print "R2D2: Coletor adicionado a lista de coletores."
            self.getClientSocket().close()
            break
        
    def listarColetores(self):
        print "Lista de coletores:\n"
        for coletor, status in self.getColetores().iteritems():
            print str(coletor) + ": " + status
    
    def enviarComando(self, comando):
        self.listarColetores()
        if self.getColetorAtual() == "":
            self.setColetorAtual(raw_input("Insira o IP de um coletor valido:"))
        
        self.getClientSocket().setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mensagem = ""
        while mensagem != "OK":
            print "Aguardando..."
            try:
                self.getClientSocket().sendto(comando, (self.getColetorAtual(), 5000))
                self.setColetorAtual("")
                mensagem, endereco = self.getClientSocket().recvfrom(2048)
                break
            
            except:
                print "..."
                continue
    
    def inserirComando(self):
        print "Comandos: LISTAR | COLETAR | SUSPENDER | CONTINUAR"
        
        while True:
            comando = ""
            listadecomandos = {"LISTAR":"", "SUSPENDER":"", "CONTINUAR":"", "COLETAR":""}
            while comando not in listadecomandos.keys():
                comando = raw_input("Insira um comando valido:")
            if comando == "LISTAR":
                self.listarColetores()
            else:
                self.enviarComando(comando)
                
            
            
        
if __name__ == '__main__':
    
    monitor = Monitor()
    monitor.inserirComando()