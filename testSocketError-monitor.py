import socket, socketerror, traceback

downloadSocket = socketerror.socketError(socket.AF_INET, socket.SOCK_DGRAM)
downloadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
downloadSocket.settimeout(2.0)
downloadSocket.setErrorProb(0.5)
file = None

def ask():
    comando = raw_input("[R2D2] Insira um comando > ")
    return comando
    
def enviarComando(comando, coletor):
    if comando != "DOWNLOAD":
        inserirComando()
    else:
        try:
            downloadSocket.settimeout(None)
            while True:
                try:
                    downloadSocket.sendWithError(comando, (coletor,6020))
                    print 'Enviou DOWNLOAD'
                    mensagem, endereco = downloadSocket.recvWithError(2048)
                    break
                except:
                    traceback.print_exc()
                    print "Monitor - Timeout"
                    continue
            downloadSocket.settimeout(None)
            mensagem = ""
            string = []
            cont = 0
            while mensagem.count("COM:THEEND") <1:
                mensagem, endereco = downloadSocket.recvWithError(2048)
                if mensagem != "nothing":
                    string.append(mensagem[3:].replace("COM:THEEND",""))
                    downloadSocket.sendWithError("NACK"+str(cont),(coletor,6020))
                    cont+=1
            file = open("log.txt", "w")
            for line in string:
                file.write(line)
            
            file.close()
            print "Download terminado com sucesso."
            downloadSocket.close()
                
        except:
            traceback.print_exc()
            print "..."

def inserirComando():
    print "\nEscolha o coletor que deseja fazer download:\n"
    coletor = ask()
    enviarComando("DOWNLOAD", coletor)
    
inserirComando()