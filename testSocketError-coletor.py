import socket, traceback
from socketerror import *

downloadSocket = socketError(socket.AF_INET, socket.SOCK_DGRAM)
downloadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
arquivoLog = "log.txt"
arq = None

def abrirArquivoLog(instrucao="a"): #se nao houver nenhuma instrucao o default eh  adicionar
    arq = open(arquivoLog,instrucao)

def fecharArquivoLog(): #se nao houver nenhuma instrucao o default eh adicionar
    arq.close()

def enviarArqLog():
    downloadSocket.bind(('', 6020))
    #print "Permissao atual = Enviar Arquivo de Log"  
    while 1:
        downloadSocket.settimeout(9999)
        #try:
        print "Esperando mensagem de download"
        #self.__downSocket.connect((self.__monitor[0], int(self.__monitor[1]) +1))
        message, clientAddress = downloadSocket.recvWithError(2048)

        if message == "DOWNLOAD":
            abrirArquivoLog("r")
            logBuffer = arq.read()                    
            fecharArquivoLog()
            partesBuffer = {}

            for i in range (0, (len(logBuffer) / 256)):
                partesBuffer["ACK"+str(i)] = logBuffer[i*256:((i+1)*256)]

            for index in range(0,len(partesBuffer.keys())):
                print index
                ACK = "ACK"+str(index)
                conteudo = partesBuffer[ACK]
                conteudo = conteudo.replace("\n","\n ")
                downloadSocket.settimeout(5)
                while not ("NACK"+str(index)) in message:
                    try:
                        if index == len(partesBuffer.keys()) -1:
                            downloadSocket.sendWithError(ACK+conteudo+"FIM", clientAddress)
                            message, clientAddress = downloadSocket.recvWithError(2048)
                        else:
                            downloadSocket.sendWithError(ACK+conteudo, clientAddress)
                            message, clientAddress = downloadSocket.recvWithError(2048)
                    except:
                        print "Timeout"