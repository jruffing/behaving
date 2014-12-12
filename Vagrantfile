# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise64"

  # shared
  config.vm.hostname = "streams-uitest"
  config.vm.synced_folder "/Users/jruffi01/", "/home/vagrant/"
  config.vm.synced_folder "/Users/jruffi01/code/bsca/behaving", "/streams_ui_test"

  # virtualbox
  if defined? VagrantVbguest
    config.vbguest.auto_update = true
  end
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--memory", "1024"]
    vb.cpus = 1
  end
end
