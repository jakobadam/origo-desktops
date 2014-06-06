# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define :ubuntu do |c|
    c.vm.box = "ubuntu14.04"
    c.vm.hostname = "ubuntu"
    c.vm.network "private_network", type: "dhcp"
    c.vm.network :forwarded_port, guest: 80, host: 8000
    c.vm.provision "shell", path: "install.sh"
    # Use NFS as a shared folder
    c.vm.synced_folder ".", "/vagrant", :nfs => true, id: "vagrant-root"
  end

  config.vm.define :windows do |c|
    c.vm.hostname = "windows-server"
    c.vm.box = "windows-2012R2"
    # c.vm.network :private_network, ip: "192.168.123.155"
    c.vm.network "private_network", type: "dhcp"

    # Use NFS as a shared folder
    # c.vm.synced_folder ".", "/vagrant", :nfs => true, id: "vagrant-root"

    # c.vm.provider "kvm" do |kvm|
    #     kvm.vnc_port = 5555
    # end

  end

end
