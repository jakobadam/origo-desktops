import os
import glob
import zipfile
import winrm
import subprocess
import logging
import winadm

from django.db import models
from django.conf import settings
from django.dispatch import receiver

log = logging.getLogger('rds')

PACKAGE_DIR = '%s' % (settings.MEDIA_ROOT)
SAMBA_SHARE = '\\\\ubuntu\\share'

print subprocess.check_output(['whereis','vagrant'])

def generate_filename(instance, filename):
    """Create a filename like firefox31/software/firefox31.exe"""
    return os.path.join(PACKAGE_DIR, instance.name, 'software', filename)

class Package(models.Model):

    VALID_FILE_TYPES = ['exe','msi','zip', 'EXE', 'MSI', 'ZIP']

    name = models.CharField(db_index=True, max_length=512)
    version = models.CharField(max_length=20)
    file = models.FileField(
        upload_to=generate_filename,
        verbose_name='File',
        help_text='File type must one of (%s)' % ', '.join(VALID_FILE_TYPES))
    message = models.TextField()

    installed = models.BooleanField(default=False)
    installed_path = models.CharField(max_length=1000, blank=True)
    
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
            f.write(self.install_cmd)

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
        return "\\".join((SAMBA_SHARE, self.name, 'log', '%s.log' % self.basename))

    @property
    def log_path(self):
        return os.path.join(self.basepath, 'log', self.name + '.log')

    @property
    def log_url(self):
        return os.path.join(settings.MEDIA_URL, self.name, 'log', self.basename + '.log')

    @property
    def install_cmd(self):
        root,ext = os.path.splitext(self.file.path)
        if ext == '.msi':
            return 'msiexec /L*+ "%s" /passive /i "%s" %s' % (self.log_samba_path, self.samba_path, self.args)
        return '"%s" %s' % (self.samba_path, self.args)

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
        """Install software on server
        """
        res = server.cmd(self.install_cmd, self.args.split())
        success = res.status_code == 0
        if success:
            self.message = 'Deployed %s. %s' % (self,res.std_out)
            self.installed = True
        else:
            self.message = 'Error deploying %s: %s' % (self,res.std_err)
            self.installed = False
        self.save()
        return success

    def _add_installed_path(self, server):
        import winadm
        path = winadm.whereis(self.name, **server.winrm_args)
        
    def _add_package_dirs(self):
        for d in ('log', 'script'):
            os.makedirs(os.path.join(self.basepath,d))
        os.chmod(os.path.join(self.basepath,'log'), 0777)

    @property
    def zipped(self):
        base, ext = os.path.splitext(self.file.path)
        return ext == '.zip'

    def unzip(self):
        assert self.zipped, "Can't unzip none zip file"
        with zipfile.ZipFile(self.file.path) as z:
            directory = os.path.join(self.basepath, 'software')
            z.extractall(directory)

    def find_installer(self):
        """Take a guess on which should be run to install
        """
        for ext in ('exe', 'EXE', 'msi', 'MSI'):
            path = os.path.join(self.basepath, 'software', '*.%s' % ext)
            files = glob.glob(path)
            if files:
                return files[0]
        return None

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
    """On Package change unzip (if zipped) and update test script
    """
    if hasattr(instance, '_file_updated'):

        if instance.zipped:
            instance.unzip()

            # We do some additional processing and don't want to
            # run the post_save again            
        delattr(instance, '_file_updated')
        
        executable = instance.find_installer()
        if executable:
            instance.file = executable
        instance.installed = False
        instance.save()
        
        instance._add_package_dirs()
    # always update test script
    instance._add_test_script()


class Helper(object):

    @classmethod
    def first_or_create(cls):
        s = cls.objects.first()
        if not s:
            s = cls.objects.create()
        return s
        
class State(models.Model, Helper):

    LOCATION_AD_TYPE = 'ad_type'
    LOCATION_AD_EXTERNAL_SETUP = 'ad_external_setup'
    LOCATION_AD_INTERNAL_SETUP = 'ad_internal_setup'    
        
    LOCATION_SERVER_WAIT = 'server_wait'
    LOCATION_SERVER_SETUP = 'server_setup'
    
    EXTERNAL = 'external'
    INTERNAL = 'internal'

    location = models.CharField(max_length=100, default=LOCATION_AD_TYPE)
    active_directory = models.CharField(max_length=100, default=INTERNAL)
    
    @classmethod
    def first_or_create(cls):
        s = cls.objects.first()
        if not s:
            s = cls.objects.create()
        return s

class ActiveDirectory(models.Model, Helper):
        
    domain = models.CharField(max_length=1000)
    user = models.CharField(max_length=200)
    # TODO: hash it? Just one anyways
    password = models.CharField(max_length=200)

class Server(models.Model):
    """The windows server to install software on

    Currently: There is only one
    """
    ip = models.IPAddressField(db_index=True)
    name = models.CharField(max_length=100, verbose_name='computer name')
    domain = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=128, verbose_name='Password')
    updated = models.BooleanField(default=False)
    
    def __str__(self):
        return self.ip

    def winrm_session(self):
        return winrm.Session(self.ip, auth=(self.user, self.password))
        
    def cmd(self, cmd, args=()):
        log.info('Running cmd: {}'.format(cmd))
        s = self.winrm_session()
        return s.run_cmd(cmd, args)

    def software(self):
        software = []
        winadm.set_session(self.winrm_session())
        res = winadm.whereis('')

        if res.status_code == 0:
            # Mozilla Firefox | C:\Program Files (x86)\Mozilla Firefox\firefox.exe
            lines = res.std_out
    
            lines = lines.split('\r\n')
            for l in lines:
                elms = l.split('|')
                if len(elms) == 2:
                    software.append({'name':elms[0],'path':elms[1]})
        return software

    def fetch_applications(self):

        winadm.set_session(self.winrm_session())
        res = winadm.whereis('')

        if res.status_code == 0:
            # Mozilla Firefox | C:\Program Files (x86)\Mozilla Firefox\firefox.exe
            lines = res.std_out.split('\r\n')
            for l in lines:
                elms = l.split('|')
                if len(elms) == 2:
                    name = elms[0]
                    path = elms[1]
                    Application.objects.get_or_create(name=name, path=path, server=self)

        # TODO: remove apps?

class Application(models.Model):

    name = models.CharField(max_length=100)
    path = models.CharField(max_length=1000)
    server = models.ForeignKey(Server)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def publish(self):
        self.published = True
        self.save()

    def unpublish(self):
        self.published = False
        self.save()
