# -*- coding: cp1252 -*-
#PARA PARAR O PROCESSO PARALELO DO COLETOR USAR sudo pkill -f r2d2-coletor.py
import os
import socket, traceback

class Coletor:
    
    def __init__(self):
        self.tamanhoPacote = 1024
        self.hostBroadcast = ''
        self.portaEnvioBroadcast = 9000
        self.portaRecebeBroadcast = 9001
        self.envioBroadcast = '<broadcast>'
        self.broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.status="0"
        
    def abrirConexao(self):
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcastSocket.settimeout(20)
        self.broadcastSocket.bind((self.hostBroadcast, self.portaRecebeBroadcast))
        
        while True:
            self.broadcastSocket.sendto("DESCOBRIR", (self.envioBroadcast, self.portaEnvioBroadcast))
            print("CP3O: Descobrindo monitor...")
            
            try:
                mensagem, endereco = self.broadcastSocket.recvfrom(2048)
                if str(mensagem) == "DESCOBERTO":
                    print "CP3O: Descoberto monitor " + str(endereco)
                    break
            except Exception:
                continue
        
    def getBroadcastSocket(self):
        return self.broadcastSocket
        
    def getTamanhoPacote(self):
        return self.tamanhoPacote
        
    def getPortaEnvioBroadcast(self):
        return self.portaEnvioBroadcast   
        
    def getStatus(self):
        return self.status
        
    def setStatus(self, status):
        self.status = status
    
    def trocaStatus(self, status):
        if status=="0":
            self.setStatus("1")
        elif status=="1":
            self.setStatus("0")
        return self.getStatus()

if __name__ == '__main__':
    
    print("C3PO: Coletor iniciado")
    
    c3po = Coletor()
    c3po.abrirConexao()
    broadcastSocket = c3po.getBroadcastSocket()
    
    mensagemMonitor, enderecoMonitor = broadcastSocket.recvfrom(c3po.getTamanhoPacote())
    print mensagemMonitor
    
    
    while True :
        try:
            mensagemComando, endereco = broadcastSocket.recvfrom(c3po.getTamanhoPacote())
            
            if mensagemComando == "CAPTURAR": #and u.getStatus() == None
                broadcastSocket.sendto("C3PO: Capturando...", endereco)
                print("C3PO: Capturando...")
                #u.start()
            
            elif mensagemComando == "PAUSAR":
                broadcastSocket.sendto("C3PO: Pausado", endereco)
                #u.setStatus(True)
            
            elif mensagemComando == "CONTINUAR":
                broadcastSocket.sendto("C3PO: Capturando...", endereco)
                #u.setStatus(False)
                
                
        except (KeyboardInterrupt, SystemExit):
             os.system('clear')
             break