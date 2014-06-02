# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define :ubuntu do |c|
    c.vm.hostname = "ubuntu-14.04-server"
    c.vm.box = "ubuntu14.04"
    c.vm.hostname = "ubuntu"
    c.vm.network :forwarded_port, guest: 8000, host: 8000

    # Use NFS as a shared folder
    c.vm.synced_folder ".", "/vagrant", :nfs => true, id: "vagrant-root"

    c.vm.provider :virtualbox do |vb|
      vb.customize ["startvm", :id, "--type", "gui"]
      vb.customize ["modifyvm", :id, "--memory", "2048"]
      vb.customize ["modifyvm", :id, "--cpus", "2"]
      vb.customize ["modifyvm", :id, "--hwvirtex", "on"]
      vb.customize ["modifyvm", :id, "--audio", "none"]
      vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
      vb.customize ["modifyvm", :id, "--nictype2", "virtio"]
    end
  end
end
