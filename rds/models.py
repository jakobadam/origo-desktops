import os
import glob
import zipfile
import winrm
import logging
import winadm
import shutil

from django.db import models
from django.conf import settings

log = logging.getLogger(__name__)

PACKAGE_DIR = '%s' % (settings.MEDIA_ROOT)
SAMBA_SHARE = '\\\\ubuntu\\share'

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

    def __str__(self):
        return self.name
                
    def save(self, *args, **kwargs):
        log.info('Saving Package {}'.format(self))
        # file updated is an attribute that is explicitly set from the view
        file_updated = kwargs.get('file_updated')
        if kwargs.has_key('file_updated'):
            del kwargs['file_updated']
        
        if self.pk:
            old_instance = Package.objects.get(pk=self.pk)
            if file_updated:
                old_instance.delete_files()            

        r = super(Package, self).save(*args, **kwargs)

        if file_updated:
            from rds import tasks
            tasks.process_upload.delay(self.pk)
        return r

    def delete(self, *args, **kwargs):
        self.delete_files()
        return super(Package, self).delete()
        
    def add_script(self):
        script_path = self._test_script_path
        with open(script_path, 'w') as f:
            f.write(self.install_cmd)

        # Make it executable
        os.chmod(self._test_script_path, 0755)
        log.info('Added install test script "{}"'.format(script_path))

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
        return os.path.join(self.basepath, 'log', self.basename + '.log')

    @property
    def log_exists(self):
        log.info(self.log_path)
        return os.path.isfile(self.log_path)

    @property
    def log_url(self):
        return os.path.join(settings.MEDIA_URL, self.name, 'log', self.basename + '.log')

    @property
    def install_cmd(self):
        root,ext = os.path.splitext(self.file.path)
        if ext == '.msi':
            return 'msiexec /L*+ "%s" /passive /i "%s" %s' % (self.log_samba_path, self.samba_path, self.args)
        return '"%s" %s' % (self.samba_path, self.args)
                
    def delete_files(self):
        """Delete software folder with install files and test files
        """
        log.info('Deleting package "{}" from filesystem'.format(self.path))
        if self.file:
            file_path = self.file.path
            if os.path.isfile(file_path):
                shutil.rmtree(self.basepath)
                return
        log.info('Trying to delete package files, but there are none "{}"'.format(self))
    
    def install(self, server):
        """Install software on server
        """
        log.info('Adding install tasks for package "{}"'.format(self))
        from rds import tasks
        tasks.install_package.delay(self.pk, server.pk)

    def uninstall(self, server):
        """Install software on server
        """
        log.info('Adding un-install tasks for package "{}"'.format(self))
        from rds import tasks
        tasks.uninstall_package.delay(self.pk, server.pk)        
        
    def add_dirs(self):
        dirs = [os.path.join(self.basepath, d) for d in ('log', 'script')]
        log.info('Creating package dirs: {}'.format(dirs))        
        for d in dirs:
            os.makedirs(d)
        os.chmod(os.path.join(self.basepath,'log'), 0777)

    @property
    def zipped(self):
        base, ext = os.path.splitext(self.file.path)
        return ext == '.zip'

    def unzip(self):
        log.info('Unzipping "{}"'.format(self.file.path))
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
    updated = models.BooleanField(default=True)
    
    def __str__(self):
        return "{} ({})".format(self.name, self.ip)

    def winrm_session(self):
        return winrm.Session(self.ip, auth=(self.user, self.password))
        
    def cmd(self, cmd, args=()):
        log.info('Running cmd: {}'.format(cmd))
        s = self.winrm_session()
        return s.run_cmd(cmd, args)

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
                
import rds.signals
rds.signals
