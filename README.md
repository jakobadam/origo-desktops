# One-Click RDP Services

## Quick Start

```
$ vagrant up ubuntu
```

Point browser to http://host:8000

## Winexe

There is a winexe wrapper available in the bin directory

I recommend putting this somewhere in your path:

```
ln -s PATH/wexe.py /usr/local/bin/wexe.py
```

Now you can run winexe command like this:
```
wexe.py -u vagrant -p vagrant -i 192.168.123.191 file whoami.bat
```


**Note:** I've had no luck accessing a share through winexe mounted
  with:
```
net use b: \\ubuntu\share
```
Instead I specify the fully qualified path.

## Vagrant

I use vagrant to setup a test environment with a Ubuntu server and
Windows server.

Install vagrant
Link here

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
