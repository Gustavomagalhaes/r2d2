#!/usr/bin/env python
import pika
import sys

credentials = pika.PlainCredentials('skywalker', 'luke')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.16.206.250', 5672, '/starwars', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Nenhuma mensagem especificada.'
channel.basic_publish(exchange = 'topic_logs', routing_key = routing_key, body = message)
print " [x] Sent %r:%r" % (routing_key, message)

connection.close()
