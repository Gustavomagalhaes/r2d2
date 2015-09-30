#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('skywalker', 'luke')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.206.250', 5672, '/starwars', credentials))
channel = connection.channel()
        
result = channel.queue_declare(exclusive = True)
queue_name = result.method.queue
        
binding_keys = ["http", "ssdp", "ssl", "dhcp", "ssh", "unknown", "all"]

#TEM QUE OLHAR ESSE FOR!        
for binding_key in binding_keys:
    result = channel.queue_declare(exclusive = True)
    queue_name = result.method.queue
    channel.queue_bind(exchange = "topic_logs", queue = queue_name, routing_key = binding_key)

print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body)

channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()
