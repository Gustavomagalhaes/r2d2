import socket,socketerror

HOST = 'localhost'
PORT = 12000
s = socketerror.socketError(socket.AF_INET, socket.SOCK_DGRAM)
s.setErrorProb(0.5)
s.connect((HOST, PORT))
s.sendWithError("teste")
data = s.recvWithError(1024)
print(data)
s.sendWithError("testando")
data = s.recvWithError(1024)
print(data)
s.close()
