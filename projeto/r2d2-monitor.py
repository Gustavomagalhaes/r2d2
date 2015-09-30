# -*- coding: cp1252 -*-
import os, sys, socket, logging
#import pika
logging.basicConfig()

class Monitor:
    
    def __init__(self):
        self.tamanhoPacote = 1024
        self.portaEnvioBroadcast = 9001
        self.portaRecebeBroadcast = 9000
        self.hostBroadcast = ''
        self.broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.coletoresConectados={}
        self.coletorAtual=""
        
        self.iniciarMonitor()
        
        self.channelRabbit = None
        #self.conexaoRabbit()
        #self.protocolos = {"http":0, "ssdp":0, "ssl":0, "dhcp":0, "ssh":0, "unknown":0, "all":0}
        
        self.status = "0"
        
    # def conexaoRabbit(self):
    #     self.credentials = pika.PlainCredentials('skywalker', 'luke') #criar user no CONSUMIDOR (receive) e permissoes no vhost
    #     self.connection = pika.BlockingConnection(pika.ConnectionParameters('IP', 5672, '/starwars', self.credentials)) #criar o vhost
    #     self.channel = self.connection.channel()
        
    #     self.result = self.channel.queue_declare(exclusive = True)
    #     self.queue_name = self.result.method.queue
        
    #     self.binding_keys = ["http", "ssdp", "ssl", "dhcp", "ssh", "unknown", "all"]
        
    #     #CHECAR O FOR QUE TA DANDO ERRO!
    #     for binding_key in self.binding_keys:
    #         self.result = self.channel.queue_declare(exclusive = True)
    #         self.queue_name = self.result.method.queue
    #         self.channel.queue_bind(exchange = "topic_logs", queue = self.queue_name, routing_key = binding_key)
    
    def iniciarMonitor(self):
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcastSocket.bind((self.hostBroadcast, self.portaRecebeBroadcast))
        
    def getTamanhoPacote(self):
        return self.tamanhoPacote
    
    def listaDeColetores(self):
        print 'R2D2: Listando coletores:'
        if self.coletoresConectados == {}:
            print "R2D2: Nenhum coletor conectado.\n"
            raw_input("<Enter> para sair")
            os.system("clear")
        else:
            keys = self.coletoresConectados.keys()
            while True:
                try:
                    for n, coletor in enumerate(keys):
                        print "(%d) - coletor %s \n" % (n+1, coletor)
                    escolha = raw_input("R2D2: Selecione o número do coletor: ")
                except:
                    print("R2D2: Coletor inválido[1].\n")
                    raw_input("R2D2: <Enter> para sair")
                    os.system("clear")
                    
                else:
                    if escolha > len(self.coletoresConectados):
                        print("R2D2: Coletor inválido[2].")
                    else:
                        break
            coletorAtual = keys[escolha-1]
            self.setColetorAtual(coletorAtual)
            
           
            
    
    def getColetorAtual(self):
        return self.coletorAtual
        
    def setColetorAtual(self, coletorAtual):
        self.coletorAtual = coletorAtual
        
    def getBroadcastSocket(self):
        return self.broadcastSocket
        
    def abrirConexoes(self):
        while True:
            try:
                print ("R2D2: Aguardando...")
                mensagemColetor, enderecoColetor = self.broadcastSocket.recvfrom(self.getTamanhoPacote())
                if mensagemColetor == "DESCOBRIR":
                    print("R2D2: Descoberto por coletor ") + str(enderecoColetor)
                    ip, porta = enderecoColetor
                    if not self.coletoresConectados.has_key(ip):
                        self.coletoresConectados[ip] = enderecoColetor
                        print ip, ' [ok]'
                    mensagemMonitor = 'DESCOBERTO'
                    self.broadcastSocket.sendto(mensagemMonitor, enderecoColetor)
                
                mensagemMonitor = 'R2D2: Aguardando comando...'
                self.broadcastSocket.sendto(mensagemMonitor, enderecoColetor)
                return False
            
            except (KeyboardInterrupt, SystemExit):
                os.system('clear')
                break
    
    
        
        
if __name__ == '__main__':
    r2d2 = Monitor()
    broadcastSocket = r2d2.getBroadcastSocket()
    
    print 'R2D2: Monitor ligado!'
    
    while True:
        print 'R2D2: Menu:'
        print '\n'
        print '[1] LISTAR COLETORES'
        print '[0] SAIR'
        print '\n'
        keyboardInput = raw_input('>> ')
        
        if keyboardInput == '1':
            r2d2.abrirConexoes()
            r2d2.listaDeColetores()
            print("Coletor" + r2d2.getColetorAtual())
            print '\n'
            print '[1] INICIAR'
            print '[2] PAUSAR'
            print '[0] SAIR'
            print '\n'
            keyboardInput = raw_input('>> ')
            os.system("clear")
            endereco = r2d2.coletoresConectados[r2d2.getColetorAtual()]
            
            if keyboardInput == "1":
                #r2d2.iniciarColeta(endereco)
                print("Coleta iniciada")
                opcao=raw_input(">> ")
                os.system('clear')      
                continue
                
            #restante...
            elif keyboardInput == "2":
                print("Coleta pausada")
                
            elif keyboardInput == "0":
                os.system("clear")
                continue
                
            else:
                raw_input("R2D2: Opção inválida.")
                os.system("clear")
                continue
        elif keyboardInput == "0":
            os.system("clear")
            break
        
        else:
            raw_input("R2D2: Opção inválida.")
            os.system("clear")
            continue
        
    broadcastSocket.close()
    print "R2D2 encerrado."
