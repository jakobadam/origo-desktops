from django.db import models
import os

import winexe

PACKAGE_DIR = '/srv/samba/'
WINDOWS_IP = '192.168.123.12'

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

    def __init__(self, *args, **kwargs):
        self._file = kwargs.get('file')
        if self._file:
            del kwargs['file']
        super(Package, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._file:
            _add_package(self._file)
        super(Package, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        _delete_package(self.name)
        super(Package, self).delete(*args, **kwargs)

    @staticmethod
    def deploy(filename):
        cmd = '"//ubuntu/share/%s" -ms' % filename
        return winexe.cmd(
            user='vagrant',
            password='vagrant',
            host=WINDOWS_IP,
            cmd=cmd)

class Server(models.Model):
    """The windows server to install software on

    Currently: There is only one
    """
    ip = models.IPAddressField()
    name = models.CharField(max_length=100, verbose_name='computer name')
    domain = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=128)


