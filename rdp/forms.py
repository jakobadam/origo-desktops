from .path import ext

from django import forms

VALID_FILE_TYPES = ['exe','msi','zip']

class PackageForm(forms.Form):

    file  = forms.FileField(required=True)

    def clean_file(self):
        file = self.cleaned_data['file']

        if not ext(file) in VALID_FILE_TYPES:
            raise forms.ValidationError('File type %s is not supported!' % ext)
