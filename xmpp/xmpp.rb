require 'rubygems'
require 'xmpp4r/client'

# Connect to the server and authenticate
jid = Jabber::JID::new('jspyconftest@ufuks-macbook-pro.local')
cl = Jabber::Client::new(jid)
cl.connect
cl.auth('12345')

# Indicate our presence to the server
cl.send Jabber::Presence::new

# Send a salutation to a given user that we're ready
salutation = Jabber::Message::new( 'jspyconftest@ufuks-macbook-pro.local', 'Hello World' )
salutation.set_type(:chat).set_id('1')
cl.send salutation 

# Add a message callback to respond to peer requests
cl.add_message_callback do |inmsg|
    # Send the response
    outmsg = Jabber::Message::new( inmsg.from, inmsg.body )
    outmsg.set_type(:chat).set_id('1')
    cl.send outmsg
end
# Run
while 1
end