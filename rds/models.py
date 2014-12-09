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

log = logging.getLogger(__name__)

RE_EXECUTABLE = re.compile('.*exe$|.*EXE$|.*MSI$|.*msi$')

def generate_filename(instance, filename):
    """Create a filename like firefox31/software/firefox31.exe"""
    return os.path.join(instance.path, 'software', filename)

class Package(models.Model):

    VALID_FILE_TYPES = ['exe','msi','zip', 'EXE', 'MSI', 'ZIP']

    name = models.CharField(
        db_index=True,
        max_length=512,
        verbose_name='Software name')

    version = models.CharField(
        max_length=20,
        verbose_name='Software version')

    file = models.FileField(
        upload_to=generate_filename,
        verbose_name='File',
        help_text='File type must one of (%s)' % ', '.join(VALID_FILE_TYPES))

    message = models.TextField()
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

        r = super(Package, self).save(*args, **kwargs)

        if file_updated:
            log.info(u'Adding task to process uploaded package {}'.format(self))
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

    @property
    def path_samba(self):
        return "\\".join((settings.SAMBA_SHARE, self.dirname))

    @property
    def dirname(self):
        filename = u'{}_{}'.format(self.name, self.version).lower()
        return text.get_valid_filename(filename)

    def samba_path_join(self, *args):
        return "\\".join(args)

    @property
    def samba_path(self):
        return self.samba_path_join(settings.SAMBA_SHARE, self.dirname)

    @property
    def samba_path_installer(self):
        # slice away /foo/bar/
        relative = self.installer[len(settings.PACKAGE_DIR)+1:]
        return self.samba_path_join(settings.SAMBA_SHARE, *relative.split('/'))

    @property
    def log_samba_path(self):
        return self.samba_path_join(self.samba_path, 'log', u'{}.log'.format(self.dirname))

    @property
    def log_path(self):
        return os.path.join(self.path, 'log', u'{}.log'.format(self.dirname))

    @property
    def log_exists(self):
        return os.path.isfile(self.log_path)

    @property
    def log_url(self):
        return os.path.join(settings.MEDIA_URL, self.name, 'log', self.basename + '.log')

    @property
    def install_cmd(self):
        if not self.installer:
            return None
        root,ext = os.path.splitext(self.installer)
        if ext == '.msi':
            return u'msiexec /L*+ "%s" /passive /i "%s" %s' % (self.log_samba_path, self.samba_path, self.args)
        return u'"%s" %s' % (self.samba_path_installer, self.args)

    def delete_files(self):
        """Delete software folder with install files and test files
        """
        log.info(u'Removing package directory "{}"'.format(self.path))
        try:
            if os.path.isdir(self.path):
                log.info(u'Removing package directory "{}"'.format(self.path))
                shutil.rmtree(self.path)
                return
        except OSError, e:
            log.error(e)
        finally:
            log.info(u'Tried deleting package, but there is no dir named "{}"'.format(self.path))

    def install(self, server):
        """Install software on server
        """
        log.info(u'Adding install task for package "{}" to worker'.format(self))
        from rds import tasks
        self.installing = True
        self.save()
        tasks.install_package.delay(self.pk, server.pk)

    def uninstall(self, server):
        """Install software on server
        """
        log.info(u'Adding un-install tasks for package "{}"'.format(self))
        from rds import tasks
        tasks.uninstall_package.delay(self.pk, server.pk)

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

    def find_executables(self):
        executables = []
        software_dir = os.path.join(self.path, 'software')
        for root, dirnames, filenames in os.walk(software_dir):
            # file_matches = [f for f in filenames if re.match(RE_EXECUTABLE, f)]
            # for f in file_matches:
            #     executables.append(os.path.join(root, f))

            # fuck it... make everything executable
            for f in filenames:
                executables.append(os.path.join(root, f))
        return executables

    def make_executable(self):
        log.info(u'Setting execution bits on: {}'.format(self))
        for f in self.find_executables():
            os.chmod(f, 0755)

    def find_installer(self):
        """Take a guess on which should be run to install
        only looks in toplevel directory
        """
        for ext in ('exe', 'EXE', 'msi', 'MSI'):
            path = os.path.join(self.path, 'software', '*.{}'.format(ext))
            log.info(u'Looking for installer with glob "{}"'.format(path))
            files = glob.glob(path)
            if files:
                installer_path = files[0]
                log.info(u'Found package installer "{}"'.format(installer_path))
                return installer_path
        log.error(u'No installer found for "{}"'.format(self))
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

    ROLE_CHOICES = (
        (RDS_SESSION_HOST, 'session host'),
        (RDS_GATEWAY, 'gateway'),
        (RDS_BROKER, 'broker'),
        (RDS_WEB, 'web')
    )

class Server(models.Model):
    """The windows server to install software on

    """
    ip = models.IPAddressField(db_index=True)
    name = models.CharField(max_length=100, verbose_name='Computer name')
    domain = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=128, verbose_name='Password')
    updated = models.BooleanField(default=True)

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

    def cmd(self, cmd, args=()):
        log.info(u'Running cmd: {}'.format(cmd))
        s = self.winrm_session()
        return s.run_cmd(cmd, args)

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

