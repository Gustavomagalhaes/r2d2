# -*- coding: cp1252 -*-
from socket import *

class Client:

    def __init__(self,serverName="",serverPort=""):

        self.__serverName = serverName
        self.__serverPort = serverPort
        self.__listaComandosValidos = {} #preencher previamente
        self.__clientSocket = socket(AF_INET, SOCK_DGRAM)

    def setServerName(self,serverName):
        self__serverName = serverName

    def setserverPort(self,serverPort):
        self__serverPort = serverPort

    def sendBroadcast(self,comando):

        destino = ('<broadcast>', 5000)
        self.__clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__clientSocket.sendto("'Hello' do client", destino)        

        while True:
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            print "IP: " + serverAddress + " |  " + modifiedMessage
         
        
    def sendUnicast(self,comando):        
                    
        if self.__serverName == "":
            self.setServerName(raw_input('Digite um IP válido: '))

        if self.__serverPort == "":
            self.setserverPort(raw_input('Digite uma porta válida: '))

        print "Iniciando conexao..."

        response = ""
        
        while response != "Granted":
            print "...",
            clientSocket.sendto("Permissao",(self.__serverName, self.__serverPort))
            response, serverAddress = clientSocket.recvfrom(2048)                

        print "Conexao bem sucedida."

        clientSocket.sendto(comando,(self.__serverName, self.__serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)    


    def listarComandos(self):
        for comando, descricao in self.__listaComandosValidos.iteritems():
            print comando + " -> " + descricao
        
    def receberComando(self):
        comando = raw_input('Insira um comando para o colector: ')
        while comando in self.__listaComandosValidos == False:
            comando = raw_input('Insira um comando para o colector: ')

        if self.__listaComandosValidos[comando] == "broadcast":
            sendBroadcast(comando)
        else:
            sendUnicast(comando)

    def verificarResposta(self):
        return ""