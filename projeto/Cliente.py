# -*- coding: cp1252 -*-
from socket import *

class Cliente:

    def __init__(self,serverName="",serverPort=""):

        self.__serverName = serverName
        self.__serverPort = serverPort
        self.__listaComandosValidos = {} #preencher previamente
        self.__clientSocket = socket(AF_INET, SOCK_DGRAM)

    def setServerName(self,serverName):
        self__serverName = serverName

    def setserverPort(self,serverPort):
        self__serverPort = serverPort

    def enviarComandoBroadcast(self,comando):

        destino = ('<broadcast>', 5000)
        self.__clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__clientSocket.sendto("Hello from client", destino)        

        while True:
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            print "IP: " + serverAddress + " |  " + modifiedMessage
         
        
    def enviarComandoUnicast(self,comando):        
                    
        if self.__serverName == "":
            self.setServerName(raw_input('Digite um IP válido: '))

        if self.__serverPort == "":
            self.setserverPort(raw_input('Digite uma porta válida: '))

        print "Estabelecendo conexao..."

        response == ""
        
        while response != "Permitido":
            print "...",
            clientSocket.sendto("Permissao",(self.__serverName, self.__serverPort))
            response, serverAddress = clientSocket.recvfrom(2048)                

        print "Conexao realizada com sucesso"

        clientSocket.sendto(comando,(self.__serverName, self.__serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)    


    def listarComandos(self):
        for comando, descricao in self.__listaComandosValidos.iteritems():
            print comando + " -> " + descricao
        
    def receberComando(self):
        comando = raw_input('Por favor digite um comando para o coletor: ')
        while comando in self.__listaComandosValidos == False:
            comando = raw_input('Por favor digite um comando para o coletor: ')

        if self.__listaComandosValidos[comando] == "broadcast":
            enviarComandoBroadcast(comando)
        else:
            enviarComandoUnicast(comando)

    def verificarResposta(self):
        return ""