# -*- coding: cp1252 -*-
import socket, traceback

serverHost = ""
serverPort = 12000
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
            print "Client wants me to stop."
            break
        else:
            print "%s from %s" % (messageClient, clientAddress)
            messageServer = "Welcome %s!" % (clientAddress)
            serverSocket.sendto(messageServer, clientAddress) 
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
