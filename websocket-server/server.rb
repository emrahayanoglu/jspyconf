require 'rubygems'
require 'em-websocket'

EM.run {
  EM::WebSocket.run(:host => "localhost", :port => 8887) do |ws|
    ws.onopen { |handshake|
      puts "WebSocket connection open"
      ws.send "Hello Client, you connected to #{handshake.path}"
    }

    ws.onclose { puts "Connection closed" }

    ws.onmessage { |msg|
      puts "Recieved message: #{msg}"
      ws.send "Pong: #{msg}"
    }
  end
}