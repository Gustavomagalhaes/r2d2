# -*- coding: cp1252 -*-
import os
import socket, traceback

class Coletor:
    
    def __init__(self):
        self.tamanhoPacote = 1024
        self.portaEnvioBroadcast = 9000
        self.portaRecebeBroadcast = 9001
        self.hostBroadcast = ''
        self.envioBroadcast = '<broadcast>'
        self.broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.abrirConexao()
        
    def abrirConexao(self):
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcastSocket.bind((self.hostBroadcast, self.portaRecebeBroadcast))
        self.broadcastSocket.sendto(b"DISCOVER", (self.envioBroadcast, self.portaEnvioBroadcast))
        
    def getBroadcastSocket(self):
        return self.broadcastSocket

if __name__ == '__main__':
    
    c3pO = Coletor()
    broadcastSocket = c3pO.getBroadcastSocket
    
    ok, enderecoServidor = broadcastSocket.recvfrom(c3pO.tamanhoPacote)
    print ok
    wait, enderecoServidor = broadcastSocket.recvfrom(c3pO.tamanhoPacote)
    print wait
    
    # while True:
        
    #     try:
    #         mensagem, endereco = broadcastSocket.recvfrom(tamanhoPacote)
    #         print "Recebido: '{0}' do IP: {1}".format(mensagem, endereco) 
    #         if message == b'ACK':
    #             print 'IP do server é {0}'.format(endereco[0])
    #     except (KeyboardInterrupt, SystemExit):
    #         u.stop()
    #         os.system('clear')
    #         break
    #     except:
    #         traceback.print_exc()