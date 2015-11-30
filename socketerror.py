import socket, random, time

class socketError(socket.socket):
    errorProb = 0.0

    def setErrorProb(self, p):
        self.errorProb = float(p)

    def getErrorProb(self):
        return self.errorProb
    
    def sendWithError(self, s):
        if (self.type == socket.SOCK_DGRAM):
            u = random.random()
            if (u>self.errorProb):
                self.send(s)
        else:
            self.send(s)

    def recvWithError(self, n):
        if (self.type == socket.SOCK_DGRAM):
            data = self.recv(n)
            u = random.random()
            if (u>self.errorProb):
                return data
            else:
                raise socket.timeout
        else:
            return self.recv(n)        
