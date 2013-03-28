import sys
import sleekxmpp
def main(): 
  bot = EchoBot("jspyconftest@jabber.org", "12345678")
  bot.run() 

class EchoBot: 
  def __init__(self, jid, password) : 
    self.xmpp = sleekxmpp.ClientXMPP(jid, password) 
    self.xmpp.add_event_handler("session_start", self.handleXMPPConnected) 
    self.xmpp.add_event_handler("message", self.handleIncomingMessage) 

  def run(self):
    self.xmpp.connect() 
    self.xmpp.process(threaded=False) 

  def handleXMPPConnected(self, event):
    print "Connected" 
    self.xmpp.sendPresence(pstatus = "Send me a message")
    self.xmpp.sendMessage("jspyconftest@jabber.org","Hello World")

  def handleIncomingMessage(self, message): 
    self.xmpp.sendMessage(message["from"], message["body"]) 

if __name__ == "__main__" :
    main()