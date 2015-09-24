# -*- coding: cp1252 -*-
import os
import socket, traceback

class Coletor:
    
    def __init__(self):
        self.tamanhoPacote = 1024
        self.portaEnvioBroadcast = 9000
        self.portaRecebeBroadcast = 9001
        self.hostBroadcast = ''
        # self.envioBroadcast = '<broadcast>'
        self.broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.abrirConexao()
        
    def abrirConexao(self):
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcastSocket.bind((self.hostBroadcast, self.portaRecebeBroadcast))
        # self.broadcastSocket.sendto(b"DISCOVER", (self.envioBroadcast, self.portaEnvioBroadcast))
        
    def getBroadcastSocket(self):
        return self.broadcastSocket

if __name__ == '__main__':
    
    c3pO = Coletor()
    c3pO.abrirConexao()
    broadcastSocket = c3pO.getBroadcastSocket()
    
    while True :
        try:
            messagem , endereco = broadcastSocket.recvfrom(c3pO.tamanhoPacote)
            print("message '{0}' from : {1}".format(messagem, endereco))
            if messagem == b'DISCOVER':
                broadcastSocket.sendto(b"ACK", (endereco[0], c3pO.portaEnvioBroadcast))
        except (KeyboardInterrupt, SystemExit):
             raise
        except:
            traceback.print_exc()