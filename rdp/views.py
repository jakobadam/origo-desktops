import os
from glob import glob

from django.shortcuts import render
from django import http
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .forms import UploadProgramForm
from .models import Package

UPLOAD_DIR = '/srv/samba/'

def _handle_upload(f):
    with open('%s%s' % (UPLOAD_DIR,f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def _list_packages():
    os.chdir(UPLOAD_DIR)
    return glob('*')

def _delete_package(package):
    os.chdir(UPLOAD_DIR)
    os.remove(package)

def add_program(request):

    if request.method == 'POST':
        form = UploadProgramForm(request.POST, request.FILES)
        if form.is_valid():
            _handle_upload(request.FILES['file'])
            return http.HttpResponseRedirect(reverse('programs'))
    else:
        form = UploadProgramForm()

    return render(request, 'add_program.html', {'form':form})

@require_http_methods(['POST'])
def delete_program(request):
    filename = request.POST['filename']
    _delete_package(filename)
    msg = 'Program %s was deleted' % filename
    messages.success(request, msg)
    return http.HttpResponseRedirect(reverse('programs'))

def programs(request):
    return render(request, 'index.html', {'packages': _list_packages()})

@require_http_methods(['POST'])
def deploy_program(request):
    filename = request.POST['filename']
    output,success = Package.deploy(filename)

    if success:
        msg = 'Deploying %s. %s' % (filename,output)
        messages.info(request, msg)
    else:
        msg = 'Error deploying %s. %s' % (filename,output)
        messages.error(request, msg)

    return http.HttpResponseRedirect(reverse('programs'))
