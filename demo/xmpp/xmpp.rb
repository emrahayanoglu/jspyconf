require 'rubygems'
require 'xmpp4r/client'
require 'amqp'

jid = Jabber::JID::new('jspyconftest@ufuks-macbook-pro.local')
cl = Jabber::Client::new(jid)
cl.connect
cl.auth('12345')

cl.send Jabber::Presence::new

EventMachine.run do
	connection = AMQP.connect(:host => '127.0.0.1', :port => 5001)
	puts "Connected to AMQP broker. Running #{AMQP::VERSION} version of the gem..."

	channel  = AMQP::Channel.new(connection)
	queueSend = channel.queue("jspyconf.send", :auto_delete => true)
	queueReceive = channel.queue("jspyconf.receive", :auto_delete => true)
	exchange = channel.direct("")

	queueSend.subscribe do |payload|
		message = Jabber::Message::new( 'jspyconftest@ufuks-macbook-pro.local', payload )
		message.set_type(:chat).set_id('1')
		cl.send message 
	end
 
	cl.add_message_callback do |inmsg|
		if inmsg.from != "jspyconftest@ufuks-macbook-pro.local"
			puts "Received Message From Jabber: #{inmsg.body}"
			exchange.publish inmsg.body, :routing_key => queueReceive.name
		end
	end
end