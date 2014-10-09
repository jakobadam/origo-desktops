import os
import shutil

from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings

from django.core.files import File

from rds.models import Package
from rds import models

test_settings = {
    'PACKAGE_DIR': settings.TEST_PACKAGE_DIR,
    'MEDIA_ROOT': settings.TEST_PACKAGE_DIR 
    }

def _add_file(package):    
    settings.SOFTWARE_ROOT = settings.BASE_DIR + '/software' 
    
    filename = 'Firefox Setup 31.0.exe'

    path = os.path.join(settings.SOFTWARE_ROOT, filename)
    test_path = models.generate_filename(package, filename)    

    assert os.path.isfile(path), "There is no file there"
    
    dirname = os.path.dirname(test_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    shutil.copy(path, test_path)
    assert os.path.isfile(test_path), "There is no file there"
    package.file = File(open(test_path))

@override_settings(**test_settings)
class TestPackage(TestCase):

    def setUp(self):
        self.name = 'Firefox'
        self.version = '31.0'
        self.args = '-ms'        

        self.p = Package(name=self.name, args=self.args, version=self.version)

    def tearDown(self):
        try:
            self.p.delete_files()
        except OSError:
            pass

    def test_path(self):
        path = self.p.path
        expected = settings.PACKAGE_DIR + '/firefox_31.0'
        self.assertEqual(path, expected)

        p = Package(name='MS Access', version='2007')
        expected = settings.PACKAGE_DIR + '/ms_access_2007'
        self.assertEqual(p.path, expected)
    
    def test_find_installer(self):
        _add_file(self.p)
        self.p.save()
        path = self.p.find_installer()
        expected = settings.PACKAGE_DIR + '/firefox_31.0/software/Firefox Setup 31.0.exe'
        self.assertEqual(path, expected)

    def test_script_path(self):        
        self.p.save()
        self.p.installer = self.p.find_installer()
        path = self.p.test_script_path
        expected = settings.PACKAGE_DIR + '/firefox_31.0/script/firefox_install.bat'
        self.assertEqual(path, expected)

    def test_log_path(self):
        expected = settings.PACKAGE_DIR + '/firefox_31.0/log/firefox_31.0.log'
        self.assertEqual(self.p.log_path, expected)
                
    def test_add_dirs(self):
        self.p.add_dirs()
        path = settings.PACKAGE_DIR + '/firefox_31.0/script'
        self.assertTrue(os.path.exists(path))
                
    def test_samba_path(self):
        samba_path = self.p.samba_path
        expected = r'\\ubuntu\share\firefox_31.0'
        self.assertEqual(samba_path, expected)

    def test_samba_path_installer(self):
        _add_file(self.p)
        self.p.save()
        self.p.installer = self.p.find_installer()
        
        samba_path = self.p.samba_path_installer
        expected = r'\\ubuntu\share\firefox_31.0\software\Firefox Setup 31.0.exe'
        self.assertEqual(samba_path, expected)
        
    def test_install_cmd(self):
        _add_file(self.p)
        self.p.save()
        self.p.installer = self.p.find_installer()

        expected = '"%s" %s' % (r"\\ubuntu\share\firefox_31.0\software\Firefox Setup 31.0.exe", self.args)
        actual = self.p.install_cmd
        self.assertEqual(actual, expected)

        
