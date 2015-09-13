import socket

site = "www.ufrpe.br"
site = "www.google.com.br"

mysock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
mysock.connect((site,80))

mysock.send("GET / HTTP/1.0\n")
mysock.send("Host: "+site+"\n")
mysock.send("\n")

while 1:
    data = mysock.recv(2048)
    if ( len(data) < 1 ):
        break
    print(data)
    
mysock.close()
