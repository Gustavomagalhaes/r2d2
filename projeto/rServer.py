# -*- coding: cp1252 -*-
import socket, traceback

serverHost = ""
serverPort = 188
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
serverSocket.bind((serverHost, serverPort))

print "SERVER PRONTO. Ctrl+C para terminar."

while 1:
    try:
        #Aguarda receber dados do socket
        messageClient, clientAddress = serverSocket.recvfrom(1024)
        if messageClient == "stop":
            print "Client solicitou parada."
            break
        else:
            print "'%s' recebido de %s pelo server." % (messageClient, str(clientAddress))
            messageServer = "Welcome"
            serverSocket.sendto(messageServer, clientAddress) 
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
