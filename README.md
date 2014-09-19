# One-Click RDP Services

## Quick Start

Install prerequisites:
* vagrant
* vagrant-kvm

```
$ vagrant up ubuntu
```

Point browser to http://host:8080

## Installing prerequsites

### Vagrant

I use vagrant to setup a test environment with a Ubuntu server and
Windows server.

Install vagrant:
```
wget https://dl.bintray.com/mitchellh/vagrant/vagrant_1.6.5_x86_64.deb
```

Install vagrant-kvm plugin

**More: Website: https://github.com/adrahon/vagrant-kvm/blob/master/README.md**
```bash
$ sudo adduser ~~usrname~~ libvirtd
$ sudo apt-get install qemu libvirt-dev libvirt-bin nfs-kernel-server nfs-common build-essential redir
$ sudo vagrant plugin install vagrant-kvm
```

To avoid libvirt permission error:
```bash
$ sudo apt-get install apparmor-profiles apparmor-utils
$ sudo aa-complain /usr/lib/libvirt/virt-aa-helper
```

## RDS

### RD Session Deployment

Components of a RD deployment are:
* RD Connection Broker
* RD Web Access
* RD Session Host(s)

### RD Session Collection

Pool of servers (session hosts) that handles connections.
