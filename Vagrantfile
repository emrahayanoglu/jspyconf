# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.box = "precise32"

  config.vm.forward_port 5672, 5001
  config.vm.forward_port 15672, 15001
end
