import socket

serverHost = '<broadcast>'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print "Digite sua mensagem:"
print "- Envie uma mensagem vazia para parar este client"
print "- 'stop' para parar todos os servidores"

# Almost infinite loop... ;)
while True:
    clientMessage = raw_input('>> ')
    if len(clientMessage) == 0:
        break
    else:
        clientSocket.sendto(clientMessage, (serverHost, serverPort))
        print "Sending message '%s'..." % clientMessage
        messageServer, serverAddress = clientSocket.recv(2048)
        print messageServer
        

clientSocket.close()
print 'Client stopped.'
