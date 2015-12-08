import socket, traceback
from socketerror import *

downloadSocket = socketError(socket.AF_INET, socket.SOCK_DGRAM)
downloadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
downloadSocket.settimeout(5)
logFile = "log.txt"
file = None
coletor = ""

def enviarComandoDownload(self):
                    
    if coletor == "":
        coletor = raw_input('Digite um IP válido: ')

    #self.__downSocket.connect((self.__serverName, int(self.__serverPort) +1))
    self.downloadSocket.settimeout(3)
    while True:
        try:
            self.downloadSocket.sendWithError("DOWNLOAD",(coletor, 6020))
            mensage, serverAddress = self.downloadSocket.recvWithError(2048)
            break            
        except:
            print "Timeout"
            continue

    self.downloadSocket.settimeout(None)
    mensage = ""
    stringBuffer = []
    cont = 0
    while mensage.count("FIM") < 1:
        mensage, serverAddress = self.downloadSocket.recvWithError(2048)
        if mensage != "nada":            
            stringBuffer.append(mensage[3:].replace("FIM",""))
            self.downloadSocket.sendWithError("NACK"+str(cont),(coletor, 6020))
            cont+=1

    coletor = ""
    arq = open("log_"+coletor+".txt","w")
    for linha in stringBuffer:
        arq.write(linha)
    arq.close()
    print "Download concluido"
    self.downloadSocket.close()