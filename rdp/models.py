from django.db import models
from django.conf import settings
from django.dispatch import receiver

import os

import winexe

from winexe.exceptions import RequestException

PACKAGE_DIR = '%s' % (settings.MEDIA_ROOT)
SAMBA_SHARE = '\\\\ubuntu\\share'

def generate_filename(instance, filename):
    """Create a filename like firefox31/software/firefox31.exe"""
    return os.path.join(PACKAGE_DIR, instance.name, 'software', filename)

class Package(models.Model):

    VALID_FILE_TYPES = ['exe','msi','zip']

    name = models.CharField(db_index=True, max_length=512)
    file = models.FileField(
        upload_to=generate_filename,
        help_text='File type must one of (%s)' % ', '.join(VALID_FILE_TYPES))
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
        script_path = self._test_script_path
        with open(script_path, 'w') as f:
            f.write(self.cmd)

        # Make it executable
        os.chmod(self._test_script_path, 0755)            

    @property
    def _test_script_path(self):
        return '%s.bat' % os.path.join(self.basepath, 'script', self.basename)

    @property
    def basepath(self):
        """Return the path to the package
        """
        return os.path.join(PACKAGE_DIR, self.name)

    @property
    def basename(self):
        return os.path.basename(self.file.path)
    
    @property
    def path(self):
        return os.path.join(PACKAGE_DIR, self.name)
                
    @property
    def samba_path(self):
        return "\\".join((SAMBA_SHARE, self.name, 'software', self.basename))

    @property
    def log_samba_path(self):
        name = os.path.basename(self.file.path)
        return "%s\\%s.log" % (LOG_DIR, name)

    @property
    def log_path(self):
        return os.path.join(self.basepath, 'log', self.name + '.log')

    @property
    def log_url(self):
        return os.path.join(settings.MEDIA_URL, 'logs', self.name + '.log')
                        
    @property
    def cmd(self):
        root,ext = os.path.splitext(self.file.path)
        if ext == '.msi':
            return 'msiexec /L*+ %s /passive /i "%s" %s' % (self.log_samba_path, self.samba_path, self.args)
        return 'cmd /c "%s" %s' % (self.samba_path, self.args)

    def file_updated(self):
        """Called from the view, which sucks...
        TODO: Register that the file is updated
        """
        self._file_updated = True
                
    def delete_files(self):
        """Delete software folder with install files and test files
        """
        import shutil
        if self.file.path:
            shutil.rmtree(self.basepath)
        else:
            raise IOError('Trying to delete package files, but there are none')
    
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
            self.installed = True
            success = True
        except RequestException, e:
            self.message = 'Error deploying %s: %s' % (self,str(e))
            self.installed = False
        self.save()
        return success

    def _add_package_dirs(self):
        for d in ('log', 'script'):
            os.makedirs(os.path.join(self.basepath,d))
        
@receiver(models.signals.post_delete, sender=Package)
def auto_delete_files_on_delete(sender, instance, **kwargs):
    """Delete relevant package files on `Package` delete
    """
    if instance.file:
        file_path = instance.file.path
        if os.path.isfile(file_path):
            instance.delete_files()
            
@receiver(models.signals.pre_save, sender=Package)
def auto_delete_old_files_on_change(sender, instance, **kwargs):
    """Delete files on `Package` update
    """
    if hasattr(instance, '_file_updated'):
        if instance.pk:
            old_instance = Package.objects.get(pk=instance.pk)
            old_instance.delete_files()

@receiver(models.signals.post_save, sender=Package)
def auto_add_files_on_change(sender, instance, **kwargs):
    print 'post_save'
    if hasattr(instance, '_file_updated'):
        instance._add_package_dirs()
        instance._add_test_script()
     
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

