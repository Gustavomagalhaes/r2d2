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
        
        broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        broadcastSocket.bind((hostBroadcast,portaRecebeBroadcast))
        
        broadcastSocket.sendto(b"DISCOVER", (envioBroadcast, portaEnvioBroadcast)

if __name__ == '__main__':
        
    while True:
        
        try:
            mensagem, endereco = broadcastSocket.recvfrom(tamanhoPacote)
            print "Recebido: '{0}' do IP: {1}".format(mensagem, endereco) 
            if message == b'ACK':
                print 'IP do server é {0}'.format(endereco[0])
        except (KeyboardInterrupt, SystemExit):
            u.stop()
            os.system('clear')
            break
        except:
            traceback.print_exc()