import os

from django.test import TestCase
from django.test import Client
from django.conf import settings

from django.core.files import File

from rdp.models import Package
from rdp import models

settings.MEDIA_ROOT = 'software'
models.PACKAGE_DIR = settings.MEDIA_ROOT

class TestPackage(TestCase):

    def setUp(self):
        self.name = 'Firefox 31'
        self.file = File(open('software/Firefox Setup 31.0.exe'))
        self.args = '-ms'
        
        self.p = Package(name=self.name, file=self.file, args=self.args)

    def test_script_path(self):
        path = self.p._test_script_path
        expected = settings.MEDIA_ROOT + '/Firefox 31/script/Firefox Setup 31.0.exe.bat'
        self.assertEqual(path, expected)

    def test_add_package_dirs(self):
        self.p.delete_files()
        self.p._add_package_dirs()
        path = 'software/Firefox 31/script'
        self.assertTrue(os.path.exists(path))
                
    def test_add_test_script(self):
        self.p.delete_files()
        self.p._add_package_dirs()
        self.p._add_test_script()
        path = 'software/Firefox 31/script/Firefox Setup 31.0.exe.bat'
        try:
            script_file = open(path)
        except IOError:
            self.fail('Expected test script at: %s' % script_file)

    def test_samba_path(self):
        samba_path = self.p.samba_path
        expected = '\\\\ubuntu\\share\\Firefox 31\\software\\Firefox Setup 31.0.exe'
        self.assertEqual(samba_path, expected)
        
    def test_cmd(self):
        expected = '"%s" %s' % ("\\\\ubuntu\\share\\Firefox 31\\software\\Firefox Setup 31.0.exe", self.args)
        actual = self.p.cmd
        self.assertEqual(actual, expected)

        
