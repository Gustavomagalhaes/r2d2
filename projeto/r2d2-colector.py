-*- coding: cp1252 -*-
import socket, traceback

AMOUNT_BYTES = 1024

BROADCAST_PORT_SEND = 9001      # Porta que o cliente estara escutando
BROADCAST_PORT_RECV = 9000      # Porta que o cliente ira enviar mensagem
BROADCAST_LISTEN = ''           #Interface que sera utilizada, se voce por 127.255.255.255, ele so respondera a chamadas locais

bsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   #UDP Protocol
bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
bsock.bind((BROADCAST_LISTEN, BROADCAST_PORT_RECV))

while True :
    try:
        message , address = bsock.recvfrom(AMOUNT_BYTES)
        print("message '{0}' from : {1}".format(message, address))
        if message == b'DISCOVER':
            bsock.sendto(b"ACK", (address[0] ,BROADCAST_PORT_SEND))
    except (KeyboardInterrupt, SystemExit):
         raise
    except:
        traceback.print_exc()