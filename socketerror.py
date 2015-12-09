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
            print u
            print 'entrou no if antes'
            if (u>self.errorProb):
                print 'enviou no socket'
                self.sendto(s)
        else:
            print 'Nao envia'
            self.sendto(s)

    def recvWithError(self, n):
        if (self.type == socket.SOCK_DGRAM):
            data = self.recv(n)
            print str(data)
            u = random.random()
            if (u>self.errorProb):
                print data
                return data
            else:
                print 'Nao recebe'
                return '', ''
        else:
            return self.recv(n)  