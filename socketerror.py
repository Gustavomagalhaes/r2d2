import socket, random, time

class socketError(socket.socket):
    errorProb = 0.0

    def setErrorProb(self, p):
        self.errorProb = float(p)

    def getErrorProb(self):
        return self.errorProb
    
    def sendWithError(self, s, address):
        if (self.type == socket.SOCK_DGRAM):
            u = random.randint(0,5)
            if (u>self.errorProb):
                print "Enviado"
                print str(address)
                print str(s)
                self.sendto(s, address)
            else:
                print "Nao enviado"
        else:
            self.send(s)

    def recvWithError(self, n):
        if (self.type == socket.SOCK_DGRAM):
            data = self.recvfrom(n)
            u = random.randint(0,5)
            if (u>self.errorProb):
                print data
                return data
            else:
                print "Nao recebido"
                return "nothing", "nothing"
                #raise socket.timeout
        else:
            return self.recv(n)        
