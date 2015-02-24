import os
import shutil

from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings

from django.core.files import File

from rds.models import (
    Package, Server, ServerRole
    )

from rds import models

test_settings = {
    'PACKAGE_DIR': settings.TEST_PACKAGE_DIR,
    'MEDIA_ROOT': settings.TEST_PACKAGE_DIR
    }

def _add_file(package):
    """
    Copy test file to settings.TEST_PACKAGE_DIR
    and add it to the package
    """
    settings.SOFTWARE_ROOT = settings.BASE_DIR + '/rds/tests/software'
    filename = 'firefox_setup_test.exe'

    path = os.path.join(settings.SOFTWARE_ROOT, filename)
    assert os.path.isfile(path), "There is no file there"

    test_path = models.generate_filename(package, filename)
    dirname = os.path.dirname(test_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    package.file = File(open(path), test_path)
    package._file_added = True

@override_settings(**test_settings)
class TestPackage(TestCase):

    def setUp(self):
        self.name = 'Firefox'
        self.version = '31.0'
        self.args = '-ms'

        self.farm = models.Farm(name='test farm')
        self.farm.save()

        self.p = Package(name=self.name, args=self.args, version=self.version)
        self.s = Server(ip='127.0.0.1', roles=ServerRole.RDS_ORCHESTRATOR, farm=self.farm)
        self.s.save()

    def tearDown(self):
        if hasattr(self.p, '_file_added'):
            self.p.delete_files()

    def test_path(self):
        path = self.p.path
        expected = settings.PACKAGE_DIR + '/firefox_31.0'
        self.assertEqual(path, expected)

        p = Package(name='MS Access', version='2007')
        expected = settings.PACKAGE_DIR + '/ms_access_2007'
        self.assertEqual(p.path, expected)

    def test_find_executables(self):
        _add_file(self.p)
        self.p.save()
        files = self.p.find_executables()
        self.assertTrue(files)

    def test_find_installer(self):
        _add_file(self.p)
        self.p.save()
        path = self.p.find_installer()
        expected = settings.PACKAGE_DIR + '/firefox_31.0/software/firefox_setup_test.exe'
        self.assertEqual(path, expected)

    def test_script_path(self):
        _add_file(self.p)
        self.p.save()
        self.p.installer = self.p.find_installer()
        path = self.p.test_script_path
        expected = settings.PACKAGE_DIR + '/firefox_31.0/script/firefox_31.0_install.bat'
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
        expected = r'\\127.0.0.1\share\firefox_31.0'
        self.assertEqual(samba_path, expected)

    def test_samba_path_installer(self):
        _add_file(self.p)
        self.p.save()
        self.p.installer = self.p.find_installer()

        samba_path = self.p.samba_path_installer
        expected = r'\\127.0.0.1\share\firefox_31.0\software\firefox_setup_test.exe'
        self.assertEqual(samba_path, expected)

    def test_install_cmd(self):
        _add_file(self.p)

        self.p.args = 'TRANSFORMS="{dirname}transform.mst"'

        self.p.save()
        self.p.installer = self.p.find_installer()

        expected = r'"\\127.0.0.1\share\firefox_31.0\software\firefox_setup_test.exe" TRANSFORMS="\\127.0.0.1\share\firefox_31.0\software\transform.mst"'
        actual = self.p.install_cmd
        self.assertEqual(actual, expected)
