# -*- coding: cp1252 -*-
from socket import *

#serverName = '127.0.0.1'
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)

#Conecta ao servidor
clientSocket.connect((serverName,serverPort))

#Recebe mensagem do usuario e envia ao servidor
message = raw_input('Digite uma frase:')
clientSocket.send(message)

#Aguarda mensagem de retorno e a imprime
modifiedMessage, addr = clientSocket.recvfrom(2048)
print("Retorno do Servidor:"+modifiedMessage)

clientSocket.close()
