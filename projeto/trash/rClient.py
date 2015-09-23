import socket

serverHost = '<broadcast>'
serverPort = 188
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print "Digite sua mensagem:"
print "- Envie uma mensagem vazia para parar este client"
print "- 'stop' para parar todos os servidores"

# Almost infinite loop... ;)
while True:
    clientMessage = raw_input('>> ')
    if len(clientMessage) == 0:
        break
    else:
        print "Enviando mensagem '%s'..." % (clientMessage)
        clientSocket.sendto(clientMessage, (serverHost, serverPort))
        messageServer = clientSocket.recv(1024)
        print "Mensagem do server: " + messageServer
        

clientSocket.close()
print 'Cliente parado.'
