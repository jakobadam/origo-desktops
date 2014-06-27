from .path import ext

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

VALID_FILE_TYPES = ['exe','msi','zip']

def _get_widget(placeholder):
    return forms.TextInput(attrs={'placeholder':placeholder})

class PackageForm(forms.Form):

    file  = forms.FileField(required=True)

    def clean_file(self):
        file = self.cleaned_data['file']

        if not ext(file) in VALID_FILE_TYPES:
            raise forms.ValidationError('File type %s is not supported!' % ext)

class RDSForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(RDSForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()

        # Moving field labels into placeholders
        layout = helper.layout = Layout()
        for field_name, field in self.fields.items():
            layout.append(Field(field_name, placeholder="foobar"))
            helper.form_show_labels = False

    windows_computer_name = forms.CharField(
        max_length=100,
        widget=_get_widget('Enter computer name'),
        error_messages={'required': 'Computer name cannot be blank'}
        )

    domain = forms.CharField(
        max_length=1024,
        widget=_get_widget('Enter domain e.g., example.com'),
        error_messages={'required': 'Domain must be set'}
        )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}),
        error_messages={'required': 'Password cannot be blank'}
        )
