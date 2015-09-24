# -*- coding: cp1252 -*-
import os
import sys
from socket import *

class Monitor:
    
    def __init__(self):
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)
    
    def listaDeColetores(self):
        print 'R2D2: Listando coletores:'
        #Implementar lista de coletores
    
    def menu(self):
        
        os.system('clear')
        
        while True:
            
            print 'R2D2: Menu:'
            print '\n'
            print '[1] LISTAR COLETORES'
            print '[0] SAIR'
            print '\n'
            
            keyboardInput = raw_input('>> ')
            os.system('clear')
            
            if keyboardInput == '1':
                r2d2.listaDeColetores()
                print '\n'
                print '[1] INICIAR'
                print '[2] PAUSAR'
                print '[0] SAIR'
                print '\n'            
                
                keyboardInput = raw_input('>> ')
                os.system('clear')
                
                if keyboardInput == '1':
                    os.system('clear')
                    #Código para começar a coletar
                    print 'R2D2: Colector iniciado'
                    print '\n'
                    print '[1] PARAR COLETAR'
                    print '[0] SAIR'
                    print '\n' 
                    
                    keyboardInput = raw_input('>> ')
                    os.system('clear')
                    
                    if keyboardInput == '1':
                        #código para parar coleta
                        print 'R2D2: Coleta parada'
                        print '\n'
                        print '[0] SAIR'
                        print '\n' 
                        
                        keyboardInput = raw_input('>> ')
                        os.system('clear')
                        
                        if keyboardInput == '0':
                            os.system('clear')
                            continue
                            
                        else:
                            print 'R2D2: Opção inválida' 
                            raw_input('>> ')
                            os.system('clear')
                            continue
                        
                    elif keyboardInput == '0':
                        os.system('clear')
                        continue
                    
                    else:
                        print 'R2D2: Opção inválida' 
                        raw_input('>> ')
                        os.system('clear')
                        continue
                
                elif keyboardInput == '2':
                    print 'R2D2: Colector pausado'
                    raw_input('>> ')
                    os.system('clear')
                    continue
                    
                elif keyboardInput == '0':
                    os.system('clear')
                    continue
                
                else:
                    print 'R2D2: Opção inválida' 
                    raw_input('>> ')
                    os.system('clear')
                    continue
                
            elif keyboardInput == '0':
                os.system('clear')
                print 'R2D2: Adeus mestre'
                raw_input('>> ')
                os.system('clear')
                break
            
            else:
                os.system('clear')
                print 'R2D2: Opção inválida' 
                raw_input('>> ')
                os.system('clear')
                continue
        
        
if __name__ == '__main__':
    r2d2 = Monitor()
    r2d2.menu()