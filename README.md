# One-Click RDP Services

## Development Quick Start

Install prerequisites:
* Download and install [vagrant](https://www.vagrantup.com/downloads.html)
* install vagrant-libvirt ```vagrant plugin install vagrant-libvirt```

Start controller server:
```
$ vagrant up ubuntu --provider=libvirt
```

Provision the server:
```
$ vagrant ssh ubuntu
$ cd /vagrant/conf
$ ./install.sh
```

Point browser to http://localhost:8080

## Images

Images are built with [Packer](//packer.io). Templates for creating
Ubuntu 14.04 Server are Windows 2012 R2 are available at
https://github.com/jakobadam/packer-qemu-templates

Note: The server running the RDS required Active Directory must be
sysprep'ed. Otherwise, Windows won't join servers to the domain due to
a duplicate id.

```

```

TODO: Add script to the Windows Packer template to setup
RDS.

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
$ runcelery.sh
```
