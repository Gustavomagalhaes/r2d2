#!/usr/bin/env python
import pika
import sys

credentials = pika.PlainCredentials('darth', 'vader')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.206.157', 5672, '/', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = ['bittorent', 'ssdp', 'http', 'ssl', 'dhcp', 'ssh', 'unknow', 'all']
if not binding_keys:
    print >> sys.stderr, "Usage: %s [binding_key]..." % (sys.argv[0],)
    sys.exit(1)

for binding_key in binding_keys:
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body,)

channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()
