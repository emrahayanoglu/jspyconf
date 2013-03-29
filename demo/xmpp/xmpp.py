import sys
import sleekxmpp
import pika
def main(): 
  bot = EchoBot("jspyconftest@ufuks-macbook-pro.local", "12345")
  bot.run() 

class EchoBot: 
  def __init__(self, jid, password) : 
    self.xmpp = sleekxmpp.ClientXMPP(jid, password) 
    self.xmpp.add_event_handler("session_start", self.handleXMPPConnected) 
    self.xmpp.add_event_handler("message", self.handleIncomingMessage) 
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5001))
    self.channelSend = self.connection.channel()
    self.channelReceive = self.connection.channel()
    self.channelSend.exchange_declare(exchange='jspyconftest.send',type='fanout')
    self.channelReceive.exchange_declare(exchange='jspyconftest.receive',type='fanout')
    self.result = self.channelSend.queue_declare(exclusive=True)
    self.queue_name = self.result.method.queue
    self.channelSend.queue_bind(exchange='jspyconftest.send',queue=self.queue_name)
    self.channelSend.basic_consume(self.callback,queue=self.queue_name,no_ack=True)
    self.channelSend.start_consuming()

  def run(self):
    self.xmpp.connect() 
    self.xmpp.process(threaded=False) 

  def handleXMPPConnected(self, event):
    print "Connected" 
    self.xmpp.sendPresence(pstatus = "Send me a message")
    self.xmpp.sendMessage("jspyconftest@ufuks-macbook-pro.local","Hello World")

  def handleIncomingMessage(self, message):
    # If message is received from the xmpp send through the receive message queue 
    self.xmpp.sendMessage(message["from"], message["body"]) 

  def callback(ch, method, properties, body):
    print " [x] %r" % (body,)
    #send message to the xmpp client
    self.xmpp.sendMessage("jspyconftest@ufuks-macbook-pro.local","Hello World")

if __name__ == "__main__" :
    main()