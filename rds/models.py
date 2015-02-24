import os
import re
import glob
import zipfile
import winrm
import logging
# import winadm
import shutil

from django.db import models
from django.conf import settings
from django.utils import text
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse

log = logging.getLogger(__name__)

RE_EXECUTABLE = re.compile('.*exe$|.*EXE$|.*MSI$|.*msi$')
RE_PACKAGE_NAME = re.compile(r'^[-a-zA-Z0-9_() .]+$')

def generate_filename(instance, filename):
    """Create a filename like firefox31/software/firefox31.exe"""
    print os.path.join(instance.path, 'software', filename)    
    return os.path.join(instance.path, 'software', filename)

SAMBA_SERVER_IP = None

class Package(models.Model):

    class Meta:
        ordering = ('name',)

    VALID_FILE_TYPES = ['exe','msi','zip', 'EXE', 'MSI', 'ZIP']

    name = models.CharField(
        db_index=True,
        max_length=512,
        verbose_name='Software name',
        validators=[RegexValidator(RE_PACKAGE_NAME, 'Use ASCII characters only')]
        )

    version = models.CharField(
        max_length=20,
        verbose_name='Software version')

    file = models.FileField(
        upload_to=generate_filename,
        verbose_name='File',
        help_text='File type must one of (%s)' % ', '.join(VALID_FILE_TYPES))

    message = models.TextField(blank=True)
    installer = models.CharField(max_length=1000, blank=True)

    # TODO: Maybe create status field instaed
    installing = models.BooleanField(default=False)
    installed = models.BooleanField(default=False)
    args = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return u'{} {}'.format(self.name,self.version)

    def save(self, *args, **kwargs):
        log.info(u'Saving Package {}'.format(self))
        # file updated is an attribute that is explicitly set from the view
        file_updated = kwargs.get('file_updated')
        if kwargs.has_key('file_updated'):
            del kwargs['file_updated']

        if self.pk:
            old_instance = Package.objects.get(pk=self.pk)
            if file_updated:
                old_instance.delete_files()

            else:
                if old_instance.args != self.args:
                    # update install script when args is updated
                    # of course also when file is updated but that is handled by
                    # process_upload
                    self.add_script()

        r = super(Package, self).save(*args, **kwargs)

        if file_updated:
            from rds import tasks
            tasks.process_upload.delay(self.pk)
        return r

    def delete(self, *args, **kwargs):
        self.delete_files()
        return super(Package, self).delete()

    def add_script(self):
        script_path = self.test_script_path
        log.info(u'Adding install test script "{}"'.format(script_path))

        with open(script_path, 'w') as f:
            f.write(self.install_cmd.encode('utf8'))

        # Make it executable
        os.chmod(self.test_script_path, 0755)

    @property
    def test_script_path(self):
        path = os.path.join(self.path, 'script', self.dirname)
        return u'{}_install.bat'.format(path)

    @property
    def path(self):
        """Return the path to the package
        """
        return os.path.join(settings.PACKAGE_DIR, self.dirname)

    # @property
    # def path_samba(self):
    #     return "\\".join((settings.SAMBA_SHARE, self.dirname))

    @property
    def samba_base_path(self):
        if not SAMBA_SERVER_IP:
            global SAMBA_SERVER_IP
            samba_server = Server.objects.filter(roles__icontains=ServerRole.RDS_ORCHESTRATOR).first()
            SAMBA_SERVER_IP = samba_server.ip
        return self.samba_path_join('\\\\' + SAMBA_SERVER_IP, 'share')

    @property
    def samba_path(self):
        """Samba path of package.
        .
        ./log
        ./software
        """
        return self.samba_path_join(self.samba_base_path, self.dirname)

    @property
    def dirname(self):
        filename = u'{}_{}'.format(self.name, self.version).lower()
        return text.get_valid_filename(filename)

    def samba_path_join(self, *args):
        return '\\'.join(args)

    @property
    def samba_path_installer(self):
        # slice away /foo/bar/
        relative = self.installer[len(settings.PACKAGE_DIR)+1:]
        return self.samba_path_join(self.samba_base_path, *relative.split('/'))

    @property
    def log_samba_path(self):
        return self.samba_path_join(self.samba_path, 'log', u'{}.log'.format(self.dirname))

    @property
    def log_path(self):
        return os.path.join(self.path, 'log', self.log_name)

    @property
    def log_name(self):
        return u'{}.log'.format(self.dirname)

    @property
    def log_exists(self):
        return os.path.isfile(self.log_path)

    @property
    def log_url(self):
        return settings.MEDIA_URL + self.log_path[len(settings.PACKAGE_DIR)+1:]
        # return os.path.join(settings.MEDIA_URL, self.name, 'log', self.log_name)

    @property
    def install_cmd(self):
        """
        Install cmd for the package

        Support for {dirname} variable in args
        """
        if not self.installer:
            return None
        args = self.args.format(dirname=self.samba_path_join(self.samba_path, 'software') + '\\')
        root,ext = os.path.splitext(self.installer)
        if ext == '.msi':
            return u'msiexec /L*+ "{}" /passive /i "{}" {}'.format(self.log_samba_path, self.samba_path_installer, args)
        return u'"{}" {}'.format(self.samba_path_installer, args)

    def delete_files(self):
        """Delete software folder with install files and test files
        """
        log.info(u'Removing package directory "{}"'.format(self.path))
        try:
            if os.path.isdir(self.path):
                shutil.rmtree(self.path)
                return
            else:
                log.info(u'Tried deleting package, but there is no dir named "{}"'.format(self.path))                
        except OSError, e:
            log.error(e)

    def install(self, server):
        """Install software on server
        """
        log.info(u'Adding install task for package "{}" to worker'.format(self))
        from rds import tasks
        self.installing = True
        self.save()
        tasks.package_install.delay(self.pk, server.pk)

    def uninstall(self, server):
        """Install software on server
        """
        log.info(u'Adding un-install tasks for package "{}"'.format(self))
        from rds import tasks
        tasks.unpackage_install.delay(self.pk, server.pk)

    def add_dirs(self):
        dirs = [os.path.join(self.path, d) for d in ('log', 'script')]
        log.info(u'Creating package dirs: {}'.format(dirs))
        for d in dirs:
            os.makedirs(d, mode=settings.FILE_UPLOAD_DIRECTORY_PERMISSIONS)
        # make it writable
        os.chmod(os.path.join(self.path,'log'), settings.FILE_UPLOAD_PERMISSIONS)

    @property
    def zipped(self):
        base, ext = os.path.splitext(self.file.path)
        return ext == '.zip'

    def unzip(self):
        log.info(u'Unzipping "{}"'.format(self.file.path))
        with zipfile.ZipFile(self.file.path) as z:
            directory = os.path.join(self.path, 'software')
            z.extractall(directory)

    def make_executable(self):
        software_dir = os.path.join(self.path, 'software')
        for dirpath, dirnames, filenames in os.walk(software_dir):
            for f in filenames:
                os.chmod(os.path.join(dirpath,f), 0755)

    def find_executables(self):
        executables = []
        for ext in ('exe', 'EXE', 'msi', 'MSI', 'bat', 'BAT'):
            path = os.path.join(self.path, 'software', '*.{}'.format(ext))
            files = glob.glob(path)
            executables.extend(files)
        log.info(u'Executables "{}"'.format(executables))
        return executables

    def guess_install_executable(self, executables):
        """Take a guess on which should be run to install
        only looks in toplevel directory
        """
        if executables:
            for path in executables:
                lowered = path.lower()
                if 'setup' in lowered or 'install' in lowered:
                    return path
            path = executables[0]
            log.info(u'No setup or install file in the package, using the first "{}"'.format(path))
            return path
        return None

    def find_installer(self):
        """Find the install executable.
        """
        executables = self.find_executables()
        installer_path = self.guess_install_executable(executables)
        if installer_path:
            log.info(u'Found package installer "{}"'.format(installer_path))
            return installer_path
        log.error('No installer found for "{}"'.format(self))
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

class ServerRole(object):

    RDS_SESSION_HOST = 'session_host'
    RDS_GATEWAY = 'gateway'
    RDS_BROKER = 'broker'
    RDS_WEB = 'web'
    RDS_AD = 'ad'
    RDS_ORCHESTRATOR = 'orchestrator'

    ROLE_CHOICES = (
        (RDS_SESSION_HOST, 'session host'),
        (RDS_GATEWAY, 'gateway'),
        (RDS_BROKER, 'broker'),
        (RDS_WEB, 'web'),
        (RDS_AD, 'ad'),
        (RDS_ORCHESTRATOR, 'orchestrator')
    )

class Farm(models.Model):

    STATUS_INSTALLING = 'installing'
    STATUS_INSTALLED = 'installed'
    STATUS_OPEN = 'open'
    
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    master = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blueprint_show', kwargs={'pk': self.pk})

class FarmPackage(models.Model):

    STATUS_INSTALLING = 'installing'
    STATUS_INSTALLED = 'installed'
    STATUS_ERROR = 'error'

    STATUS_CHOICES = (
        (STATUS_INSTALLING, STATUS_INSTALLING),
        (STATUS_INSTALLED , STATUS_INSTALLED),
        (STATUS_ERROR     , STATUS_ERROR),
        )

    farm = models.ForeignKey(Farm, related_name='farm_packages')
    package = models.ForeignKey(Package, related_name='farm_packages')
    status = models.CharField(max_length=100, blank=True, choices=STATUS_CHOICES)

    def __str__(self):
        return u'{} farm {}'.format(self.package, self.farm)

class Server(models.Model):

    class Meta:
        ordering = ['name']

    ip = models.IPAddressField(db_index=True)
    name = models.CharField(max_length=100, verbose_name='Computer name')
    domain = models.CharField(max_length=100, blank=True)
    user = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=128, verbose_name='Password', blank=True)
    updated = models.BooleanField(default=True)
    farm = models.ForeignKey(Farm, related_name='servers')

    # denormalized one-to-many model server roles
    # comma-separated list of roles
    roles = models.CharField(max_length=100)

    def __str__(self):
        return "{} ({})".format(self.name, self.ip)

    def has_role(self, role):
        for r in self.roles.split(','):
            if r == role:
                return True
        return False

    def add_role(self, role):
        roles = self.roles.split(',')
        roles.append(role)
        self.roles = ','.join(roles)

    def remove_role(self, role):
        """TODO
        """
        pass

    def winrm_session(self):
        return winrm.Session(self.ip, auth=(self.user, self.password))

    def cmd(self, cmd):
        log.info(u'Running cmd: {}'.format(cmd))
        s = self.winrm_session()
        return s.run_cmd(cmd)

    def fetch_applications(self):

        # winadm.set_session(self.winrm_session())
        # res = winadm.whereis('')

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


