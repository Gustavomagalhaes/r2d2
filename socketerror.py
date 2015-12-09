import socket, random, time

class socketError(socket.socket):
    errorProb = 0.0

    def setErrorProb(self, p):
        self.errorProb = float(p)

    def getErrorProb(self):
        return self.errorProb
    
    def sendWithError(self, s, e):
        if (self.type == socket.SOCK_DGRAM):
            u = random.random()
            if (u>self.errorProb):
                self.sendto(s, e)
        else:
            print 'Nao envia'
            self.sendto(s, e)

    def recvWithError(self, n):
        if (self.type == socket.SOCK_DGRAM):
            data = self.recvfrom(n)
            print str(data)
            u = random.random()
            if (u>self.errorProb):
                return data
            else:
                print 'Nao recebe'
                return '', ''
        else:
            return self.recvfrom(n)  