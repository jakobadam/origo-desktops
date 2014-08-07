from django.db import models
import os

import winexe

PACKAGE_DIR = '/srv/samba/'
SAMBA_SHARE = '//ubuntu/share/'

def _add_package(f):
    """Saves package in package dir
    """
    with open('%s%s' % (PACKAGE_DIR,f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def _delete_package(filename):
    """Delete package from package dir
    """
    os.chdir(PACKAGE_DIR)
    os.remove(filename)

class Package(models.Model):

    name = models.CharField(max_length=512)
    message = models.TextField()
    installed = models.BooleanField(default=False)
    args = models.CharField(max_length=1000)

    def __init__(self, *args, **kwargs):
        self._file = kwargs.get('file')
        if self._file:
            del kwargs['file']
        super(Package, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def samba_path(self):
        return "%s%s" % (SAMBA_SHARE, self.name)
    
    def save(self, *args, **kwargs):
        if self._file:
            _add_package(self._file)
        super(Package, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        _delete_package(self.name)
        super(Package, self).delete(*args, **kwargs)

    def deploy(self, server):
        cmd = '"%s" -ms' % self.samba_path
        return winexe.cmd(
            cmd,
            user=server.user,
            password=server.password,
            host=server.ip)


class Server(models.Model):
    """The windows server to install software on

    Currently: There is only one
    """
    ip = models.IPAddressField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='computer name')
    domain = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.ip

