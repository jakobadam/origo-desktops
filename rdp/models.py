from django.db import models
from django.conf import settings

import os

import winexe

from winexe.exceptions import RequestException

PACKAGE_DIR = '%s/software' % (settings.MEDIA_ROOT)
LOG_DIR = '%s/logs' % (settings.MEDIA_ROOT)
SAMBA_SHARE = '\\\\ubuntu\\share'
UPLOAD_TO = 'software'

class Package(models.Model):

    name = models.CharField(db_index=True, max_length=512)

    # MEDIA_ROOT/software
    file = models.FileField(upload_to=UPLOAD_TO)
    message = models.TextField()
    installed = models.BooleanField(default=False)
    args = models.CharField(max_length=1000, blank=True)

    # def __init__(self, *args, **kwargs):
    #     self._file = kwargs.get('file')
    #     if self._file:
    #         del kwargs['file']
    #     super(Package, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name
        
    def _add_test_script(self):
        with open(self._test_script_path, 'w') as f:
            f.write(self.cmd)
        os.chmod(self._test_script_path, 0755)            

    def _delete_test_script(self):
        os.remove(self._test_script_path)

    @property
    def _test_script_path(self):
        name = os.path.basename(self.file.path)
        return '%s.bat' % os.path.join(settings.MEDIA_ROOT, 'scripts', name)
        
    @property
    def path(self):
        return os.path.join(PACKAGE_DIR, self.name)        
                
    @property
    def samba_path(self):
        name = os.path.basename(self.file.path)
        return "%s\\%s\\%s" % (SAMBA_SHARE, UPLOAD_TO, name)

    @property
    def log_samba_path(self):
        name = os.path.basename(self.file.path)
        return "%s\\%s.log" % (LOG_DIR, name)

    @property
    def log_path(self):
        name = os.path.basename(self.file.path)
        return os.path.join(LOG_DIR, name + '.log')

    @property
    def log_url(self):
        name = os.path.basename(self.file.path)
        return os.path.join(settings.MEDIA_URL, 'logs', name + '.log')
                        
    @property
    def cmd(self):
        root,ext = os.path.splitext(self.file.path)
        if ext == '.msi':
            return 'msiexec /L*+ %s /passive /i "%s" %s' % (self.log_samba_path, self.samba_path, self.args)
        return 'cmd /c "%s" %s' % (self.samba_path, self.args)

    def save(self, *args, **kwargs):
        super(Package, self).save(*args, **kwargs)
        self._add_test_script()

    def delete(self, *args, **kwargs):
        super(Package, self).delete(*args, **kwargs)
        self._delete_test_script()

    def deploy(self, server):
        cmd = '"%s" %s' % (self.samba_path, self.args)
        success = False

        try:
            output = winexe.cmd(
                cmd,
                user=server.user,
                password=server.password,
                host=server.ip)
            self.message = 'Deployed %s. %s' % (self,output)
            success = True
        except RequestException, e:
            self.message = 'Error deploying %s: %s' % (self,str(e))

        self.save()
        return success

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

