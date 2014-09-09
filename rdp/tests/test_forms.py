from django.test import TestCase
from django.conf import settings

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from rdp.forms import PackageForm
from rdp import models

settings.MEDIA_ROOT = 'software'
models.PACKAGE_DIR = settings.MEDIA_ROOT

class TestPackageForm(TestCase):

    def setUp(self):
        f = File(open('software/Firefox Setup 31.0.exe'))        
        self.FILES = {
            'file': SimpleUploadedFile(f.name, f.read())
            }

    def test_form(self):
        POST = {
            'args': '-ms',
            'name': 'Firefox',
            }
        self.form = PackageForm(POST, self.FILES)
        self.assertTrue(self.form.is_valid())

    def test_enforce_naming(self):
        POST = {
            'args': '-ms',
            'name': ' F ',
            }
        self.form = PackageForm(POST, self.FILES)
        self.form.is_valid()
        self.assertEqual(self.form.cleaned_data['name'], 'F')
        
        
        

        
