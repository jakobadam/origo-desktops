# Origo Desktops: One-Click Remote Desktop Services

Windows Remote Desktop Services (RDS) provides access to native Windows apps from anywhere. This is great, but setting up the infrastructure is difficult; handling software deployment and scaling as you go even more so.
Windows Server 2012 R2 provides most of the pieces of a powerful RDS setup, but the setup is thoroughly cumbersome to get right. 

We aim to improve this with Origo Desktops.

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

### Install Active Directory

```bash
$ vagrant up ad
$ AD_IP=$(vagrant ssh-config ad | grep HostName | awk '{print $2}')
$ cd scripts

# The active directory server is `sysprep`'ed, otherwise since we use the same base image
# additional Windows servers will bitch about duplicate SIDs..
$ winrm vagrant@${AD_IP} < install/sysprep.bat

# Server restarts. Fill in the needed information in the GUI. 
# And rename the server, e.g., rename to ad:
$ winrm vagrant@$AD_IP -a ad < name.ps1

# rename requires restart
$ winrm vagrant@$AD_IP 'shutdown /r /t 0'

# Install ad role
$ winrm -a vagrant -a adm.example.com -a V@grant vagrant@${AD_IP} < install/ad-install.ps1
```

Above I'm using winrm from the host machine. Winrm is already installed on the `ubuntu` machine, to install it on the host machine run:
```
$ pip install -e git+https://github.com/jakobadam/pywinrm@cli#egg=pywinrm
```

Note: I have an outstanding pull-request in the upstream pywinrm repo: https://github.com/diyan/pywinrm/pull/42. Therefore I pip install the branch.



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
