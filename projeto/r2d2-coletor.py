# -*- coding: cp1252 -*-
import os
import socket, traceback

class Coletor:
    
    def __init__(self):
        self.tamanhoPacote = 1024
        self.portaEnvioBroadcast = 9000
        self.portaRecebeBroadcast = 9001
        self.hostBroadcast = ''
        self.broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def abrirConexao(self):
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcastSocket.bind((self.hostBroadcast, self.portaRecebeBroadcast))
        
    def getBroadcastSocket(self):
        return self.broadcastSocket
        
    def getTamanhoPacote(self):
        return self.tamanhoPacote
        
    def getPortaEnvioBroadcast(self):
        return self.portaEnvioBroadcast    

if __name__ == '__main__':
    
    c3pO = Coletor()
    c3pO.abrirConexao()
    
    while True :
        try:
            print 'test 1'
            mensagem, endereco = c3pO.getBroadcastSocket().recvfrom(c3pO.getTamanhoPacote())
            print 'test 2'
            print("mensagem '{0}' de : {1}".format(mensagem, endereco))
            if mensagem == b'DISCOVER':
                c3pO.getBroadcastSocket().sendto(b"ACK", (endereco[0], c3pO.getPortaEnvioBroadcast()))
        except (KeyboardInterrupt, SystemExit):
             raise
        except:
            traceback.print_exc()