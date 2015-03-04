from django.test import TestCase
from django.conf import settings

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from rds.forms import (PackageForm, ServerForm)
from rds import models

settings.MEDIA_ROOT = 'software'
models.PACKAGE_DIR = settings.MEDIA_ROOT

class TestPackageForm(TestCase):

    def setUp(self):
        self.farm = models.Farm(name='test farm')
        self.farm.save()

        f = File(open('rds/tests/software/firefox_setup_test.exe'))
        self.FILES = {
            'file': SimpleUploadedFile(f.name, f.read())
            }

    def test_form(self):
        POST = {
            'args': '-ms',
            'name': 'Firefox',
            'version': '31.0',
            'farm': self.farm.pk
            }
        self.form = PackageForm(POST, self.FILES)
        self.assertTrue(self.form.is_valid(), str(self.form))

    def test_enforce_naming(self):
        POST = {
            'args': '-ms',
            'name': ' F ',
            }
        self.form = PackageForm(POST, self.FILES)
        self.form.is_valid()
        self.assertEqual(self.form.cleaned_data['name'], 'F')


class TestServerForm(TestCase):

    def setUp(self):
        self.farm = models.Farm(name='test farm')
        self.farm.save()

    def test_form(self):
        POST = {
            'ip': '127.0.0.1',
            'name': 'RDS',
            'domain': 'example.com',
            'user': 'Administrator',
            'password': 'V@grant',
            'roles': 'orchestrator',
            'farm': self.farm.pk
            }
        self.form = ServerForm(POST)
        self.assertTrue(self.form.is_valid(), self.form.errors)
