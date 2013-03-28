require 'rubygems'
require 'amqp'
require 'em-websocket'

EM.run {
  connection = AMQP.connect(:host => '127.0.0.1', :port => 5001)
  puts "Connected to AMQP broker. Running #{AMQP::VERSION} version of the gem..."
 
  channel  = AMQP::Channel.new(connection)
  queueSend = channel.queue("jspyconf.send", :auto_delete => true)
  queueReceive = channel.queue("jspyconf.receive", :auto_delete => true)
  exchange = channel.direct("")

  EM::WebSocket.run(:host => "localhost", :port => 8887) do |ws|
    consumer = AMQP::Consumer.new(channel, queueReceive)
    ws.onopen { |handshake|
      puts "WebSocket connection open"
      ws.send "Hello Client, you connected to #{handshake.path}"
    }

    ws.onclose { puts "Connection closed" }

    ws.onmessage { |msg|
      puts "Recieved message: #{msg}"
      exchange.publish msg, :routing_key => queueSend.name
    }

    consumer.consume.on_delivery do |metadata, payload|
      puts "Message Received: #{payload}"
      ws.send payload
    end
  end
}