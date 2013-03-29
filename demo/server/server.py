import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import pika
import sys 
 
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        self.write_message("Hello World")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', port=5001))
        self.channelSend = connection.channel()
        self.channelReceive = connection.channel()
        self.channelSend.exchange_declare(exchange='jspyconftest.send',
                         type='fanout')
        self.channelReceive.exchange_declare(exchange='jspyconftest.receive',
                         type='fanout')
        self.result = channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        self.channelReceive.queue_bind(exchange='jspyconftest.receive',
                   queue=queue_name)
        self.channelReceive.basic_consume(callback,
                              queue=self.queue_name,
                              no_ack=True)
        self.channelReceive.start_consuming()
      
    def on_message(self, message):
        print 'message received %s' % message
        #send message through the send message queue
        self.channelSend.basic_publish(exchange='jspyconftest.send',
                      routing_key='',
                      body=message)

    def callback(ch, method, properties, body):
        print " [x] %r" % (body,)
        #send message back to the websocket
 
    def on_close(self):
        print 'connection closed'
 
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()