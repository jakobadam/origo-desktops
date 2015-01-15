# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define :ubuntu do |c|
    c.vm.box = "ubuntu14"
    c.vm.box_url = "https://dl.dropboxusercontent.com/u/835753/ubuntu-1404-server-vagrant-kvm.box"
    c.vm.hostname = "ubuntu"

    # Private networks doesn't work at the moment
    # c.vm.network :private_network, ip: "192.168.50.10"

    # nginx
    c.vm.network :forwarded_port, guest: 80, host: 8080
    c.vm.synced_folder ".", "/vagrant", :nfs => true, id: "vagrant-root"
  end

  config.vm.define :rds do |c|
    c.vm.hostname = "rds"
    c.vm.box_url = "http://192.168.50.137/rds.box"
    c.vm.box = "rds"
    c.vm.guest = :windows

    # c.vm.synced_folder ".", "/cygdrive/c/vagrant", type: "rsync", rsync__exclude: [".hg/", "software"]
    # c.vm.synced_folder ".", "/vagrant", :type => "smb"

    # Forward IIS
    # c.vm.network :forwarded_port, guest: 80, host: 8001
  end

  config.vm.define :sh1 do |c|
    c.vm.box_url = "http://192.168.50.137/windows-2012R2.box"
    c.vm.box = "windows-2012R2"
    c.vm.guest = :windows
  end

  config.vm.define :ad do |c|
    c.vm.box_url = "http://192.168.50.137/windows-ad.box"
    c.vm.box = "windows-ad"
    c.vm.guest = :windows
  end

  config.vm.define :windows do |c|
    # Uhh. Works now:)
    # c.vm.hostname = "test"
    c.vm.box_url = "http://192.168.50.137/windows-2012R2.box"
    # c.vm.box_url = "file:///srv/boxes/windows-2012R2.box"
    c.vm.box = "windows-2012R2"
    c.vm.guest = :windows

    # 
    # c.vm.synced_folder ".", "S:", :nfs => true, id: "vagrant-root"

    # Works, but sub-optimal due to manual sync
    # c.vm.synced_folder ".", "/cygdrive/c/vagrant", type: "rsync", rsync__exclude: [".hg/", "software"]

    # Would prefer this, but is not supported
    # c.vm.synced_folder ".", "/vagrant", :type => "smb"

    # Forward rdp
    c.vm.network :forwarded_port, guest: 3389, host: 3389
  end

  config.vm.define :windows2 do |c|
    c.vm.box = "windows-2012-R2-1"
    c.vm.guest = :windows
  end

end
