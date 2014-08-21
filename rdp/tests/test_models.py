from django.test import TestCase
from django.test import Client
from django.conf import settings

from django.core.files import File

from ..models import Package

class TestPackage(TestCase):

    def setUp(self):
        self.name = 'Firefox 31'
        self.file = File(open('software/Firefox Setup 31.0.exe'))
        self.args = '-ms'
        
        self.p = Package(name=self.name, file=self.file, args=self.args)

    def test_script_path(self):
        path = self.p._test_script_path
        expected = settings.MEDIA_ROOT + '/scripts/Firefox Setup 31.0.exe.bat'
        self.assertEqual(path, expected)
        
    def test_add_test_script(self):
        self.p._add_test_script()

    def test_delete_test_script(self):
        self.p._add_test_script()
        self.p._delete_test_script()

    def test_samba_path(self):
        samba_path = self.p.samba_path
        expected = '//ubuntu/share/software/Firefox Setup 31.0.exe'
        self.assertEqual(samba_path, expected)

        
    def test_cmd(self):
        expected = 'cmd /c "%s" %s' % ("//ubuntu/share/software/Firefox Setup 31.0.exe", self.args)
        actual = self.p.cmd
        self.assertEqual(actual, expected)
