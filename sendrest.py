import pika
import sys
import os
from threading import Thread

class sendrest(Thread):
        
    def __init__(self):
        
        Thread.__init__(self)
        self.__credentials = pika.PlainCredentials('skywalker', 'luke')
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
                       '192.168.25.61', 5672, '/starwars', self.__credentials))
        self.__channel = self.__connection.channel()
        self.__porcentagem = {"todos":0, "elefante":0, "rato":0, "tartaruga":0, "libelula":0, "caramujo":0, "guepardo":0} 
            
    def getPorcentagem(self):
        return self.__porcentagem
        
    def run(self):
        self.__channel.exchange_declare(exchange='topic_logs',
                                     type='topic')
        result = self.__channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        self.__channel.basic_consume(self.callback, queue=queue_name, no_ack=True)
        queue_name = result.method.queue
        
    def callback(self, ch, method, properties, body):
        
        animais = body.split("|")
        
        for animal in animais:
            self.__porcentagem[animal] +=1
            self.__porcentagem["todos"] +=1
            
            