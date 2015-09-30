# -*- coding: cp1252 -*-
#PARA PARAR O PROCESSO PARALELO DO COLETOR USAR sudo pkill -f r2d2-coletor.py
import os
import socket, traceback
from thread import *

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
        self.broadcastSocket.settimeout(10)
        self.broadcastSocket.bind((self.hostBroadcast, self.portaRecebeBroadcast))
        
        while True:
            self.broadcastSocket.sendto("DESCOBRIR", (self.envioBroadcast, self.portaEnvioBroadcast))
            print("CP3O: Descobrindo monitor...")
            
            try:
                mensagem, endereco = self.broadcastSocket.recvfrom(2048)
                if str(mensagem) == "DESCOBERTO":
                    print "CP3O: Descoberto monitor " + str(endereco)
                    self.broadcastSocket.settimeout(None)
                    mensagemMonitor = 'C3PO: Aguardando comando...' #primeira msg recebida pelo coletor quando o comando for passado
                    self.broadcastSocket.sendto(mensagemMonitor, endereco)
                    return False
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
    
    
    #thread = Thread()
    
    while True :
        try:
            mensagemComando, endereco = broadcastSocket.recvfrom(c3po.getTamanhoPacote())
            
            if mensagemComando == "CAPTURAR": # and thread.getStatus() == None:
                broadcastSocket.sendto("C3PO: Capturando...", endereco)
                print("C3PO: Capturando...")
                #thread.start()
                
            elif mensagemComando == "CAPTURAR": # and thread.getStatus() == False:
                broadcastSocket.sendto("C3PO: Capturando...", endereco)
                
            elif mensagemComando == "CAPTURAR": # and thread.getStatus() == True:
                broadcastSocket.sendto("C3PO: Capturando...", endereco)
                #thread.setStatus(False)
            
            elif mensagemComando == "SUSPENDER":
                broadcastSocket.sendto("C3PO: Suspenso", endereco)
                print("C3PO: Supenso")
                #thread.setStatus(True)
            
            elif mensagemComando == "CONTINUAR":
                broadcastSocket.sendto("C3PO: Capturando...", endereco)
                #thread.setStatus(False)
                
                
        except (KeyboardInterrupt, SystemExit):
             os.system('clear')
             break