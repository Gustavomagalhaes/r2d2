import pika
import sys
import os
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming import DStream
from math import sqrt

credentials = pika.PlainCredentials('skywalker', 'luke')
connection = pika.BlockingConnection(pika.ConnectionParameters(
               '192.168.25.57', 5672, '/starwars', credentials))
channel = connection.channel()

#exchange - onde os produtores publicam suas mensagens
channel.exchange_declare(exchange='topic_logs',
                         type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = ["http", "ssdp", "ssl", "dhcp", "ssh", "unknown", "all"]

protocolos = {}

global dadosRate
dadosRate = []

for binding_key in binding_keys:
    channel.queue_bind(exchange = "topic_logs", queue = queue_name, routing_key = binding_key)
    
print("[*] Waitinf for logs. To exit press CTRL+C")


<<<<<<< HEAD

=======
>>>>>>> 3cb758fb7a0bb5aad03a9420d91aa8c87877321d
def calculoRates():
    
    m,v=[],[]
    somaTamanho, somaVelocidade, somaTaxa = 0.0,0.0,0.0
    for dado in dadosRate:
        somaTamanho += dado[0] 
        somaVelocidade += dado[1]
        somaTaxa +=dado[2]
    
    mTamanho = somaTamanho/float(len(dadosRate))
    mVelocidade = somaVelocidade / float(len(dadosRate))
    mTaxa = somaTaxa / float(len(dadosRate))
    
    medias = [mTamanho, mVelocidade, mTaxa]
    
    dTamanho, dVelocidade, dTaxa = 0.0,0.0,0.0
    for dado in dadosRate:
        dTamanho += (dado[0] - mTamanho)**2
        dVelocidade += (dado[1] - mVelocidade)**2
        dTaxa += (dado[2] - mTaxa)**2
        
    desvioTamanho = sqrt(dTamanho / float(len(dadosRate)))
    desvioVelocidade = sqrt(dVelocidade /float(len(dadosRate)))
    desvioTaxa = sqrt(dTaxa /float(len(dadosRate)))
    
    desvios = [desvioTamanho, desvioVelocidade, desvioTaxa]
    
    return medias, desvios

def classificar(body):
    valoreBody = body.split("#")
    dados = [float(valoreBody[0]), float(valoreBody[1]), float(valoreBody[2])]
    dadosRate.append(dados)
    medias, desvios = calculoRates()
    
    dadosClassificados = []
    
    if(dados[0]>(medias[0] + 3 * desvios[0])):
        dadosClassificados.append("elefante")
    else:
        dadosClassificados.append("rato")
        

    if((dados[1] > (medias[1] + 3* desvios[1]) or dados[1]>900000)):
        dadosClassificados.append("tartaruga")
        
    else: 
        dadosClassificados.append("libelula")
    
    if(dados[2]<=(medias[2]+ 3*desvios[2])):
        dadosClassificados.append("caramujo")
    
    else:
        dadosClassificados.append("guepardo")
    
    return dadosClassificados
    
    
def callback(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body,)
    
    dadosClassificados = classificar(body)
    
    mensagem = dadosClassificados[0] + "|" + dadosClassificados[1] + "|" + dadosClassificados[2]    
<<<<<<< HEAD
    connection = pika.BlockingConnection(pika.ConnectionParameters( '192.168.25.57', 5672, '/starwars', credentials))
=======
    connection = pika.BlockingConnection(pika.ConnectionParameters( '172.16.206.250', 5672, '/starwars', credentials))
>>>>>>> 3cb758fb7a0bb5aad03a9420d91aa8c87877321d
    channel = connection.channel()
    channel.exchange_declare(exchange='topic_logs',type='topic')
    channel.basic_publish(exchange='topic_logs',routing_key=method.routing_key,body=mensagem)
    channel.basic_publish(exchange='topic_logs',routing_key="TODOS",body=mensagem)    
    print " [x] Sent %r:%r" % (method.routing_key, mensagem)    
    connection.close()
  
   
channel.basic_consume(callback, queue=queue_name, no_ack=True)

<<<<<<< HEAD
sc = SparkContext("spark://192.168.25.57:7077","consumer")
ssc = StreamingContext(sc, 1)
CSR = DStream(channel.start_consuming())
ssc.start()
ssc.awaitTermination()
=======
sc = SparkContext("spark://172.16.207.155:8088","consumer")
ssc = StreamingContext(sc, 1)
CSR = DStream(channel.start_consuming())
ssc.start()
ssc.awaitTermination()
>>>>>>> 3cb758fb7a0bb5aad03a9420d91aa8c87877321d
