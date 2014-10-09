import os
import shutil

from django.test import TestCase
from django.test import Client
from django.conf import settings

from django.core.files import File

from rds.models import Package
from rds import models

SOFTWARE_ROOT = settings.BASE_DIR + '/software'
TEST_MEDIA_ROOT = settings.MEDIA_ROOT = settings.BASE_DIR + '/software_test'

models.PACKAGE_DIR = TEST_MEDIA_ROOT

class TestPackage(TestCase):

    def setUp(self):
        self.filename = 'Firefox Setup 31.0.exe'
        self.name = 'Firefox'
        self.version = '31.0'
        self.args = '-ms'        

        self.p = Package(name=self.name, args=self.args, version=self.version)

    def _add_file(self):
        path = os.path.join(SOFTWARE_ROOT, self.filename)
        test_path = models.generate_filename(self.p, self.filename)
        print 'test_path', test_path
        
        dirname = os.path.dirname(test_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        shutil.copy(path, test_path)

        self.p.file = File(test_path)

    def test_path(self):
        path = self.p.path
        expected = TEST_MEDIA_ROOT + '/firefox_31.0'
        self.assertEqual(path, expected)
    
    def test_find_installer(self):
        self._add_file()
        self.p.save()
        path = self.p.find_installer()
        expected = TEST_MEDIA_ROOT + '/firefox_31.0/software/Firefox Setup 31.0.exe'
        self.assertEqual(path, expected)

    def test_script_path(self):        
        self.p.save()
        self.p.installer = self.p.find_installer()
        path = self.p._test_script_path
        expected = settings.MEDIA_ROOT + '/firefox_31.0/script/firefox_install.bat'
        self.assertEqual(path, expected)
                
    def test_add_dirs(self):
        try:
            self.p.delete_files()
        except OSError:
            pass
        self.p.add_dirs()
        path = settings.MEDIA_ROOT + '/firefox_31.0/script'
        self.assertTrue(os.path.exists(path))
                
    def test_samba_path(self):
        samba_path = self.p.samba_path
        expected = r'\\ubuntu\share\firefox_31.0'
        self.assertEqual(samba_path, expected)

    def test_samba_path_installer(self):
        self._add_file()
        self.p.save()
        self.p.installer = self.p.find_installer()
        
        samba_path = self.p.samba_path_installer
        expected = r'\\ubuntu\share\firefox_31.0\software\Firefox Setup 31.0.exe'
        self.assertEqual(samba_path, expected)
        
    def test_install_cmd(self):
        self._add_file()
        self.p.save()
        self.p.installer = self.p.find_installer()

        expected = '"%s" %s' % (r"\\ubuntu\share\firefox_31.0\software\Firefox Setup 31.0.exe", self.args)
        actual = self.p.install_cmd
        self.assertEqual(actual, expected)

        
