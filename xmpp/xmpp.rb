require 'rubygems'
require 'xmpp4r/client'
# Create a *very* simple dictionary using a hash
hash = {}
hash['ruby'] = 'Greatest little object oriented scripting language'
hash['xmpp4r'] = 'Simple XMPP library for ruby'
hash['xmpp'] = 'Extensible Messaging and Presence Protocol'

# Connect to the server and authenticate
jid = Jabber::JID::new('jspyconftest@jabber.org')
cl = Jabber::Client::new(jid)
cl.connect
cl.auth('12345678')

# Indicate our presence to the server
cl.send Jabber::Presence::new

# Send a salutation to a given user that we're ready
salutation = Jabber::Message::new( 'jspyconftest@jabber.org', 'DictBot ready' )
salutation.set_type(:chat).set_id('1')
cl.send salutation 

# Add a message callback to respond to peer requests
cl.add_message_callback do |inmsg|
    # Lookup the word in the dictionary
    resp = hash[inmsg.body]
    if resp == nil
      resp = "don't know about " + inmsg.body
    end

    # Send the response
    outmsg = Jabber::Message::new( inmsg.from, resp )
    outmsg.set_type(:chat).set_id('1')
    cl.send outmsg
end
# Run
while 1
end