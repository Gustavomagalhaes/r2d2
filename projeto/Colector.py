import pcap, dpkt, re
import time

class Colector:

    def __init__(self,expressoesRegulares,arquivoLog):
        
        self.__expressoesRegulares = expressoesRegulares
        self.__arquivoLog = arquivoLog
        self.__arq = None
        self.__protocolsApp = {}        
        self.__protocolsRede = {"IP": dpkt.ip.IP, "ARP": dpkt.arp.ARP}
        self.__protocolsTransp = {"UDP": dpkt.udp.UDP, "TCP": dpkt.tcp.TCP}        
        self.gerarProtocolos()

    def gerarProtocolos(self):

        for nome,expr in self.__expressoesRegulares.iteritems():
            self.__protocolsApp[nome] = re.compile(expr)

    def classificarApp(self,app):
        for name,p in self.__protocolsApp.iteritems():
            if p.search(app):            
                print "Application Layer = "+name
                #self.__arq.write(...)

    def classificarRede(self,red):
        for name,p in self.__protocolsRede.iteritems():
            if isinstance(red,p):
                print "Network Layer = "+name
                #self.__arq.write(...)


    def classificarTransporte(self,transp):
        for name,p in self.__protocolsTransp.iteritems():
            if isinstance(transp,p):
                print "Transport Layer = "+name
                #self.__arq.write(...)

    def abrirArquivoLog(self,instrucao="a"): #se nao houver nenhuma instrucao o default eh adicionar
        self.__arq = open(self.__arquivoLog,instrucao)

    def fecharArquivoLog(self): #se nao houver nenhuma instrucao o default eh adicionar
        self.__arq.close()

    def iniciarColeta(self,arquivo = None,timeMaximo = 45): #Se nao haver nenhum arquivo e nenhum tempo de funcionamento especificado o default eh de 60 segundos
        try:
            self.abrirArquivoLog()
            ini = time.time()
            maxi = 1
            for ts, pkt in pcap.pcap(arquivo):

                atual = time.time()
                if atual - ini > timeMaximo:
                    break

                enl = dpkt.ethernet.Ethernet(pkt) #extraindo dados do pacote
                print "Pacote %i. Data Link Layer = Ethernet" %(maxi)
                #self.__arq.write(...)
                red = enl.data

                if type(red) != type (""): 
                    self.classificarRede(red)  
                    transp = red.data

                    if type(transp) != type (""):            
                        self.classificarTransporte(transp)
                        app = transp.data
                        self.classificarApp(app)

                maxi +=1
            self.fecharArquivoLog()
        except(KeyboardInterrupt, SystemExit):
            self.fecharArquivoLog()                

        self.fecharArquivoLog()
        

expressoesRegulares = {"dropbox":"^\x7b\x22\x68\x6f","nbns":"\x01\x10\x00\x01","dhcp":"^[\x01\x02][\x01- ]\x06.*c\x82sc","http":"[\x09-\x0d -~]*"}
coletor = Colector(expressoesRegulares,"log.txt")
coletor.iniciarColeta()
#coletor.iniciarColeta("test.pcap")
