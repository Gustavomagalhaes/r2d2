import pika
import sys
import os

credentials = pika.PlainCredentials('skywalker', 'luke')
connection = pika.BlockingConnection(pika.ConnectionParameters(
               '192.168.43.69', 5672, '/starwars', credentials))
channel = connection.channel()

#exchange - onde os produtores publicam suas mensagens
channel.exchange_declare(exchange='topic_logs', type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = ["http", "ssdp", "ssl", "dhcp", "ssh", "unknown", "all"]

protocolos = {}

for binding_key in binding_keys:
    channel.queue_bind(exchange = "topic_logs", queue = queue_name, routing_key = binding_key)
    
print("Aguardando. CTRL+C para sair")

def callback(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body,)
    tamanho = body.split("|")
    tamanho = tamanho[-1]
    tamanho = tamanho.split(":")
    tamanho = tamanho[-1]

    tempo = body.split("|")
    tempo = tempo[-2]
    tempo = tempo.split(":")
    tempo = tempo[-1]
    tempo = float(tempo)
    if protocolos.has_key(method.routing_key):
        protocolos[method.routing_key]["tamanho"] += int(tamanho)
        protocolos[method.routing_key]["quantidade"] += 1
        protocolos[method.routing_key]["ultimo"] = tempo+0.00001
    else:
        protocolos[method.routing_key] = {"tamanho": int(tamanho), "quantidade": 1, "ultimo": tempo+0.00001, "primeiro": tempo}

    print "Quantidade: %i , Tamanho Total: %i " % (protocolos[method.routing_key]["quantidade"], protocolos[method.routing_key]["tamanho"])
    print "Vazao media: %f" %(protocolos[method.routing_key]["quantidade"] / (protocolos[method.routing_key]["ultimo"] - protocolos[method.routing_key]["primeiro"]))
    print "Media: %f" %(protocolos[method.routing_key]["tamanho"] / protocolos[method.routing_key]["quantidade"])
    
channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()