from django import forms

class UploadProgramForm(forms.Form):

    filename = forms.CharField(max_length=100, required=True)
    file  = forms.FileField(required=True)
