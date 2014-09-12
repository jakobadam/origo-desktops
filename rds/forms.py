import os
from django import forms

from django_password_strength.widgets import PasswordStrengthInput

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.helper import FormHelper

from .models import Server, Package


def _get_widget(placeholder):
    return forms.TextInput(attrs={'placeholder':placeholder})

class PackageForm(forms.ModelForm):

    class Meta:
        model = Package
        exclude = ['message', 'installed']

    def __init__(self, *args, **kwargs):
        super(PackageForm, self).__init__(*args, **kwargs)
        
        if self.instance.pk:
            self.fields['name'].widget.attrs['readonly'] = True
        
    def clean_file(self):
        file = self.cleaned_data['file']
        file_root, file_ext = os.path.splitext(file.name)
        # drop the . in .exe
        file_ext = file_ext[1:]
        if not file_ext in Package.VALID_FILE_TYPES:
            msg = '%s not supported! Must be %s' % (file_ext,', '.join(Package.VALID_FILE_TYPES))
            raise forms.ValidationError(msg)
        return file

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.strip()

class RenameForm(forms.Form):

    windows_computer_name = forms.CharField(
        max_length=100,
        widget=_get_widget('Enter computer name'),
        error_messages={'required': 'Computer name cannot be blank'}
        )

class DomainForm(forms.Form):

    domain = forms.CharField(
        max_length=1024,
        widget=_get_widget('Enter domain e.g., example.com'),
        error_messages={'required': 'Domain must be set'}
        )

class PasswordForm(forms.Form):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}),
        error_messages={'required': 'Password cannot be blank'}
        )

class JoinForm(forms.Form):

    ip = forms.IPAddressField()
    name = forms.CharField()
    domain = forms.CharField(required=False)
    
class ServerForm(forms.ModelForm):

    class Meta:
        model = Server
        exclude = ('user',)
        
        widgets = {
            'ip': forms.TextInput(attrs={'readonly':True}),
            'name': _get_widget('Enter computer name'),
            'domain': _get_widget('Enter FQDN e.g., example.com'),
            'user': _get_widget('Enter desired windows user name'),
            'password': PasswordStrengthInput(attrs={'placeholder':'Enter password'})
        }
        error_messages = {
            'name':{'required': 'Computer name cannot be blank'},
            'domain':{'required': 'Domain must be set'},
            'password':{'required': 'Password cannot be blank'}
        }

    # def is_valid(self):
    #     print 'is_valid!!!'
    #     super(ServerForm, self).is_valid()

    # def clean_name(self):
    #     print 'in clean name!!!'
    #     raise forms.ValidationError('Required')

    # def clean_password(self):
    #     raise forms.ValidationError('Required')
    #         # password = self.cleaned_data['password']
    #         # if not password:
    #         #     raise forms.ValidationError('Required')
    #         # return password


    # def __init__(self. *args, **kwargs):
    #     super(ServerForm, self).__init__(*args, **kwargs)
