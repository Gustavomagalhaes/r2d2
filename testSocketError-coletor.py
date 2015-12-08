import socket, socketerror, traceback

downloadSocket = socketerror.socketError(socket.AF_INET, socket.SOCK_DGRAM)
downloadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
downloadSocket.bind(("",6020))
logFile = "log.txt"
file = None

def openLog(comando = "a"):
    file = open(logFile, comando)
        
def closeLog():
    file.close()
    
while True:
    print "Aguardando download"
    downloadSocket.settimeout(10)
    mensagem, endereco = downloadSocket.recvWithError(8192)
    
    if mensagem == "DOWNLOAD":
        print "Msg DOWNLOAD recebida"
        openLog("r")
        print "Abriu log"
        temp = open(logFile, "r").read()
        print "Leu log"
        closeLog()
        print "fechou log"
        buffers = {}
        
        try:
            print "entrou no try"
            print str(temp)
            for i in range(0, (len(temp)/256)):
                print "Entrou no for i"
                buffers["ACK"+str(i)] = temp[i*256:((i+1)*256)]
                print "Adicionado " + "ACK"+str(i) + temp[i*256:((i+1)*256)] + "aos buffers"
            
            for index in range(0, len(buffers.keys())):
                print "entrou no for index"
                ACK = "ACK"+str(index)
                print "ACK: " + ACK
                content = buffers[ACK]
                content = content.replace("\n", "\n ")
                print "CONTENT: " + content
                downloadSocket.settimeout(None)
                while not ("NACK"+str(index)) in mensagem:
                    try:
                        if index == len(buffers.keys()) -1:
                            downloadSocket.sendWithError(ACK+content+"COM:THEEND", endereco)
                            print "Pacote final " + ACK+content+"COM:THEEND" + " para " + str(endereco)
                            mensagem, endereco = downloadSocket.recvWithError(8192)
                        else:
                            downloadSocket.sendWithError(ACK+content, endereco)
                            print mensagem
                            print "Enviou " + ACK+content + " para " + str(endereco)
                            mensagem, endereco = downloadSocket.recvWithError(8192)
                    except:
                        traceback.print_exc()
                        print "Nao conseguiu enviar no ACK-NACK - Timeout"
        except:
            traceback.print_exc()
            print "Nem entrou no try do add buffers - caiu no except"