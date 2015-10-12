# -*- coding: cp1252 -*-
import os, sys, socket, logging
import pika
logging.basicConfig()

class Monitor:
    
    def __init__(self):
        self.tamanhoPacote = 1024
        self.portaEnvioBroadcast = 9001
        self.portaRecebeBroadcast = 9000
        self.hostBroadcast = ''
        self.broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.coletoresConectados={}

    def iniciarMonitor(self):
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcastSocket.bind((self.hostBroadcast, self.portaRecebeBroadcast))
        
        while True:
            try:
                
                message, address = self.broadcastSocket.recvfrom(2048)
                
                if message == "MONITOR":
                    if address[0] not in  self.coletoresConectados.keys():
                        self.coletoresConectados[(address[0])] = "Coletando"
                    self.broadcastSocket.sendto("APRESENTAR", address)
            
            except (KeyboardInterrupt, SystemExit):
                self.broadcastSocket.close()
                
    def receberComando(self):
        comandos = {"LISTAR": "Lista coletores conectados", "CONTINUAR": "Continua a coleta em um coletor parado", "PARAR": "Para a coleta de um coletor"}
        print("Lista de comandos:")
        for nome, desc in comandos.iteritems():
            print("-" + nome + ": " + desc)
        print("\n")
        
        while True:
            escolha = ""
            while escolha not in comandos.keys():
                escolha = raw_input("Escolha um comando da lista de comandos: ")

            if escolha !="LISTAR":
                print"LISTAR"
            else:
                self.listarColetores()
        
        
    def listarColetores(self):
        print("Coletores conectados: ")
        for coletor, status in self.getColetoresConectados().iteritems():
            print("-" + str(coletor) + ": " + status)
        print("\n")
    
    def getColetoresConectados(self):
        return self.coletoresConectados
        
    def getBroadcastSocket(self):
        return self.broadcastSocket
    
    def getPortaEnvioBroadcast(self):
        return self.portaEnvioBroadcast
        
if __name__ == '__main__':
    r2d2 = Monitor()
    r2d2.iniciarMonitor()
    r2d2.receberComando()