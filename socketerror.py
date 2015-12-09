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
            print u
            print 'entrou no if antes'
            if (u>self.errorProb):
                print 'enviou no socket'
                self.sendto(s, e)
        else:
            print 'Nao envia'
            self.sendto(s)

    def recvWithError(self, n):
        if (self.type == socket.SOCK_DGRAM):
            mensagem, endereco = self.recvfrom(n)
            print mensagem, endereco
            u = random.random()
            if (u>self.errorProb):
                print mensagem, endereco
                return n
            else:
                print 'Nao recebe'
                return '', ''
        else:
            return self.recvfrom(n)  