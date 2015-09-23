import socket

tamanhoPkt = 1024

portaEnvioBC = 9000
portaRecebBC = 9001
hostBC = ''
envioBC = '<broadcast>'

#SOCKET PARA RECEBER MSG
bsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
bsock.bind((hostBC,portaRecebBC))

bsock.sendto(b"DISCOVER", (envioBC, portaEnvioBC))
while True :
    message , address = bsock.recvfrom(tamanhoPkt)
    if message == b'ACK':
        print("IP server is {0}".format(address[0]))