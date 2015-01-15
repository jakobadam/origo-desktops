from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings

from rds import models
from rds.models import Package
from rds import tasks

from rds.tests.test_models import _add_file

settings.PACKAGE_DIR = settings.TEST_PACKAGE_DIR
settings.PACKAGE_DIR = settings.MEDIA_ROOT

conf = {
    'PACKAGE_DIR': settings.TEST_PACKAGE_DIR,
    'MEDIA_ROOT': settings.TEST_PACKAGE_DIR 
    }

models.SAMBA_SERVER_IP = '127.0.0.1'

@override_settings(**conf)
class TestPackageTasks(TestCase):

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

    def test_process_upload(self):
        try:
            self.p.delete_files()
        except OSError:
            pass
        _add_file(self.p)
        self.p.save()
        tasks.process_upload(self.p.pk)

        try:
            open(self.p.test_script_path)
        except IOError:
            self.fail('Expected test script at: %s' % self.p.test_script_path)
