#!/usr/bin/env ruby
# encoding: utf-8
 
require "rubygems"
require "amqp"
 
EventMachine.run do
  connection = AMQP.connect(:host => 'localhost', :port => 5001)
  puts "Connected to AMQP broker. Running #{AMQP::VERSION} version of the gem..."
 
  channel  = AMQP::Channel.new(connection)
  queue    = channel.queue("amqpgem.examples.helloworld")
 
  queue.subscribe do |payload|
    puts "Received a message: #{payload}. Disconnecting..."
  end
end	