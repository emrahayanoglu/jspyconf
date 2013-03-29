import sys
import sleekxmpp
def main(): 
  bot = EchoBot("jspyconftest@ufuks-macbook-pro.local", "12345")
  bot.run() 

class EchoBot: 
  def __init__(self, jid, password) : 
    self.xmpp = sleekxmpp.ClientXMPP(jid, password) 
    self.xmpp.add_event_handler("session_start", self.handleXMPPConnected) 
    self.xmpp.add_event_handler("message", self.handleIncomingMessage) 
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5001))
    self.channelSend = connection.channel()
    self.channelReceive = connection.channel()
    self.channelSend.exchange_declare(exchange='jspyconftest.send',
                     type='fanout')
    self.channelReceive.exchange_declare(exchange='jspyconftest.receive',
                     type='fanout')

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

if __name__ == "__main__" :
    main()