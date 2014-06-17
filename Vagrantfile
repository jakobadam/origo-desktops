# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define :ubuntu do |c|
    c.vm.box = "ubuntu14.04"
    c.vm.hostname = "ubuntu"
    c.vm.network :private_network, ip: "192.168.123.10"
    c.vm.network :forwarded_port, guest: 80, host: 8000
    c.vm.synced_folder ".", "/vagrant", :nfs => true, id: "vagrant-root"
    c.vm.provision "shell", path: "install.sh"
  end


  config.vm.define :windows do |c|
    c.vm.hostname = "windows-server"
    c.vm.box = "windows-2012R2"

    # Static network stuff seems not to work for windows
    # Hmm. When setting type to dhcp we ssh into the ubuntu machine 
    # c.vm.network :private_network, type: "dhcp"

    c.vm.network :private_network, ip: "192.168.123.191"

    c.vm.network :forwarded_port, guest: 3389, host: 3389
    c.vm.network :forwarded_port, guest: 80, host: 8001

    # Use NFS as a shared folder
    # c.vm.synced_folder ".", "/vagrant", :nfs => true, id: "vagrant-root"

    # c.vm.provider "kvm" do |kvm|
    #     kvm.vnc_port = 5555
    # end

  end

end
