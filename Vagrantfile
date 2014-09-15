# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define :ubuntu do |c|
    c.vm.box = "ubuntu14"
    c.vm.box_url = "https://dl.dropboxusercontent.com/u/835753/ubuntu-14.04-server-vagrant-kvm.box"
    c.vm.hostname = "ubuntu"
    # c.vm.network :private_network, ip: "192.168.123.10"

    # nginx
    c.vm.network :forwarded_port, guest: 80, host: 8080

    # django dev server directly (when started)
    c.vm.network :forwarded_port, guest: 8000, host: 8000

    c.vm.synced_folder ".", "/vagrant", :nfs => true, id: "vagrant-root"
    c.vm.provision "shell", path: "conf/install.sh"
  end

  config.vm.define :rds do |c|
    c.vm.hostname = "rds"
    c.vm.box = "windows-2012R2"
    c.vm.box_url = "file:///srv/boxes/windows-2012R2.box"
    c.vm.guest = :windows
    # c.vm.box = "rds"

    # Forward rdp
    c.vm.network :forwarded_port, guest: 3389, host: 3389
    # Forward IIS
    c.vm.network :forwarded_port, guest: 80, host: 8001
  end

  config.vm.define :windows do |c|
    c.vm.hostname = "windows-server"
    c.vm.box_url = "file:///srv/boxes/windows-2012R2.box"
    c.vm.box = "windows-2012R2"
    c.vm.guest = :windows
  end

end
