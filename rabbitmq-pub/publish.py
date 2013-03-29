import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port=5001))
channel = connection.channel()

channel.exchange_declare(exchange='jspyconf.helloworld2',
                         type='fanout')

message = "Hello World!"
channel.basic_publish(exchange='jspyconf.helloworld2',
                      routing_key='',
                      body=message)
print " [x] Sent %r" % (message,)
connection.close()