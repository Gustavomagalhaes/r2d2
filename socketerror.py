import socket, random, time

class socketError(socket.socket):
    errorProb = 0.0

    def setErrorProb(self, p):
        self.errorProb = float(p)

    def getErrorProb(self):
        return self.errorProb
    
    def sendWithError(self, mensagem, endereco):
        if (self.type == socket.SOCK_DGRAM):
            u = random.random()
            if (u>self.errorProb):
                self.sendto(mensagem, endereco)
        else:
            self.sendto(mensagem, endereco)

    def recvWithError(self, n=8192):
        if (self.type == socket.SOCK_DGRAM):
            mensagem, endereco = self.recvfrom(n)
            data = mensagem, endereco
            u = random.random()
            if (u>self.errorProb):
                return data
            else:
                raise socket.timeout
        else:
            return self.recvfrom(n)