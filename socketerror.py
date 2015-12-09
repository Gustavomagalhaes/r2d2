import socket, random, time

class socketError(socket.socket):
    errorProb = 0

    def setErrorProb(self, p):
        self.errorProb = float(p)

    def getErrorProb(self):
        return self.errorProb
    
    def sendWithError(self, s,adress):
        if (self.type == socket.SOCK_DGRAM):
            u = random.randint(0,10)
            if (u>self.errorProb):
                print "Enviado"
                self.sendto(s,adress)
            else:
                print "Nao enviado - Aguarde o timeout do temporalizador"
        else:
            self.send(s)

    def recvWithError(self, n):
        if (self.type == socket.SOCK_DGRAM):
            data = self.recvfrom(n)
            u = random.randint(0,10)
            if (u>self.errorProb):
                print data
                return data
            else:
                print "Nao recebido - Aguarde o timeout do temporalizador"
                return "nada","nada"
        else:
            return self.recv(n)        
