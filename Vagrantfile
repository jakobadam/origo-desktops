# -*- mode: ruby -*-

Vagrant.configure("2") do |config|

  config.vm.define :ubuntu do |c|
    c.vm.box = "ubuntu-1404-server"
    c.vm.box_url = "//static.aarhusworks.com/boxes/ubuntu-1404-server.box"
    c.vm.hostname = "ubuntu"

    c.vm.provider :libvirt do |domain|
      domain.memory = 2048
      domain.cpus = 2
    end

    # port 80 on localhost:8080
    c.vm.network :forwarded_port, guest: 80, host: 8080

    # access Django directly
    # port 8000 on localhost:8000
    c.vm.network :forwarded_port, guest: 8000, host: 8000

    # dev server hangs
    c.vm.synced_folder ".", "/vagrant", :nfs => true

    # slow slow slow
    #c.vm.synced_folder ".", "/vagrant", :type => '9p'

    # not available
    # c.vm.synced_folder ".", "/vagrant", :type => 'rsync-auto'

    #c.vm.provision "shell", path: "conf/install.sh"
  end

  config.vm.define :rds do |c|
    c.vm.hostname = "rds"
    c.vm.box_url = "//static.aarhusworks.com/boxes/windows-2012R2-standard-amd64.box"
    c.vm.box = "rds"
    c.vm.guest = :windows

    c.vm.communicator = "winrm"
    c.ssh.insert_key = false

    # c.vm.synced_folder ".", "/cygdrive/c/vagrant", type: "rsync", rsync__exclude: [".hg/", "software"]
    # c.vm.synced_folder ".", "/vagrant", :type => "smb"

    # Forward IIS
    # c.vm.network :forwarded_port, guest: 80, host: 8001
  end

  config.vm.define :ad do |c|
    c.vm.box_url = "/srv/boxes/windows-2012R2-ad.box"
    c.vm.box = "ad"
    c.vm.guest = :windows
    c.vm.communicator = "winrm"

    # something is wrong with the vagrant keys?!?
    c.vm.synced_folder ".", "/vagrant", disabled: true
    #c.ssh.password = "V@grant"
    c.winrm.password = "V@grant"

    # c.vm.network :private_network, ip: "192.168.121.10"

    c.ssh.insert_key = true

    c.vm.provider :libvirt do |domain|
      domain.memory = 2048
      domain.cpus = 2
    end
  end

  config.vm.define :sh1 do |c|
    c.vm.box_url = "http://192.168.50.63/windows-2012R2.box"
    c.vm.box = "windows-2012R2"
    c.vm.guest = :windows
  end


  config.vm.define :windows do |c|
    c.vm.box_url = "/srv/boxes/windows-2012R2.box"
    c.vm.box = "windows-2012R2"
    c.vm.guest = :windows
    c.vm.communicator = "winrm"

    c.vm.provider :libvirt do |domain|
      domain.memory = 2024
      domain.cpus = 2
    end

    # c.vm.synced_folder ".", "S:", :nfs => true, id: "vagrant-root"

    # Works, but sub-optimal due to manual sync
    #c.vm.synced_folder ".", "/cygdrive/c/vagrant", type: "rsync", rsync__exclude: [".hg/", "software"]

    # Would prefer this, but is not supported
    # c.vm.synced_folder ".", "/vagrant", :type => "smb"

    # Forward rdp
    #c.vm.network :forwarded_port, guest: 3389, host: 3389
  end

  config.vm.define :windows2 do |c|
    c.vm.box_url = "http://192.168.50.63/windows-2012R2.box"
    c.vm.box = "windows-2012R2"
    c.vm.guest = :windows
    c.ssh.insert_key = false

    c.vm.provider :libvirt do |domain|
      domain.memory = 4048
      domain.cpus = 2
    end
    c.vm.network :forwarded_port, guest: 3389, host: 3389
  end

end
