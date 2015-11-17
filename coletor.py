# -*- coding: cp1252 -*-
#PARA PARAR O PROCESSO PARALELO DO COLETOR USAR sudo pkill -f coletor.py
import os, socket, traceback, sys, threading
from various import Various


class Coletor():
    
    def __init__(self):
        
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.settimeout(20)
        self.run()
        
        #self.localizarMonitor()
    
    def run(self):
        coletor = threading.Thread(target=self.localizarMonitor)
        coletor.start()
        
    def getServerSocket(self):
        return self.serverSocket

    def localizarMonitor(self):
        serverSocket = self.getServerSocket()
        
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        serverSocket.bind(('', 5000))
        
        print "[C3PO] Procurando monitor..."
    
        while 1:
            try:
                mensagem, endereco = serverSocket.recvfrom(8192)
                if mensagem == "MONITOR":
                    print "[C3PO] Monitor %s localizado" % (str(endereco))
                    serverSocket.sendto("[C3PO] Aguardando comandos.", endereco)
                    self.serverSocket.settimeout(0)
                    #print "[C3PO] Aguardando..."
                    comando = threading.Thread(target=self.receberComando(endereco))
                    comando.start()
                    break
                else:
                    continue
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                traceback.print_exc()
                #print "[C3PO] Ainda procurando monitor..."
        serverSocket.close()
    
    def receberComando(self, monitor):
        
        serverSocket = self.getServerSocket()
        
        print "[C3PO] Aguardando comando do monitor..."
    
        while 1:
            try:
                
                mensagem, endereco = self.serverSocket.recvfrom(8192)
                print mensagem
                print endereco
                if mensagem == "COLETAR":# and yoda.getStatus() == None:
                    self.serverSocket.sendto("[C3PO] Capturando...", endereco)
                    print "[C3PO] Capturando"
                   # yoda.start()
                    
                elif mensagem == "COLETAR":# and yoda.getStatus() == False:
                    self.serverSocket.sendto("[C3PO] Capturando...", endereco)
                  #  yoda.setStatus(True)
                
                elif mensagem == "COLETAR":# and yoda.getStatus() == True:
                    self.serverSocket.sendto("[C3PO] Capturando...", endereco)
                    
                elif mensagem == "SUSPENDER":
                    self.serverSocket.sendto("[C3PO] Coleta suspensa.", endereco)
                  #  yoda.setStatus(False)
                    
                elif mensagem == "CONTINUAR":
                    self.serverSocket.sendto("[C3PO] Coleta retomada.", endereco)
                  #  yoda.setStatus(True)
                    
                print "OK"
                
                self.serverSocket.sendto("OK", endereco)
            except (KeyboardInterrupt, SystemExit):
              #  yoda.stop()
                break

if __name__ == '__main__':
    
    coletor = Coletor()
    #coletorThread = threading.Thread(target=coletor.start)
    #coletorThread.start()
    #comandoThread = threading.Thread(target=coletor.run, args=())