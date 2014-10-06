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
$ wget https://dl.bintray.com/mitchellh/vagrant/vagrant_1.6.5_x86_64.deb
$ sudo dpkg -i vagrant_1.6.5_x86_64.deb
```

Install vagrant-kvm plugin

**More: Website: https://github.com/adrahon/vagrant-kvm/blob/master/README.md**
```bash
PACKAGES="
bsdtar
gcc
git
libvirt-bin
libvirt-dev
libxml2-dev
libxslt-dev
nfs-kernel-server
qemu
qemu-kvm
ruby2.0-dev
redir"
sudo apt-get -y install $PACKAGES
```

```
sudo vagrant plugin install vagrant-kvm
```

Otherwise complains about permission errors:
```
sudo aa-complain /usr/lib/libvirt/virt-aa-helper
```

Add user to libvirtd group:
```
groups $USER | grep 'libvirtd' || adduser $USER kvm
```

su - $USER

## RDS

### RD Session Deployment

Components of a RD deployment are:
* RD Connection Broker
* RD Web Access
* RD Session Host(s)

### RD Session Collection

Pool of servers (session hosts) that handles connections.

## Celery

```
celery -A rds worker -l info
```
