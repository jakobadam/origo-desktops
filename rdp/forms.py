from .path import ext

from django import forms

VALID_FILE_TYPES = ['exe','msi','zip']

class PackageForm(forms.Form):

    file  = forms.FileField(required=True)

    def clean_file(self):
        file = self.cleaned_data['file']

        if not ext(file) in VALID_FILE_TYPES:
            raise forms.ValidationError('File type %s is not supported!' % ext)

class RDSForm(forms.Form):

    # def __init__(self, *args, **kwargs):
    #     super(RDSForm, self).__init__(*args, **kwargs)
        
    # helper = self.helper = FormHelper()

    # # Moving field labels into placeholders
    # layout = helper.layout = Layout()
    # for field_name, field in self.fields.items():
    #     layout.append(Field(field_name, placeholder=field.label))
    # helper.form_show_labels = False

    windows_computer_name = forms.CharField(max_length=100, help_text="foobar")
    domain = forms.CharField(max_length=1024)
    password = forms.CharField(widget=forms.PasswordInput())
