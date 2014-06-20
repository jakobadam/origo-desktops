import os
from glob import glob

from django import shortcuts
from django import http
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .forms import PackageForm
from .models import Package

PACKAGE_DIR = '/srv/samba/'

def add_program(request):
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            p = Package(file=file, name=file.name)
            p.save()
            return http.HttpResponseRedirect(reverse('programs'))
    else:
        form = PackageForm()

    return shortcuts.render(request, 'add_program.html', {'form':form})

@require_http_methods(['POST'])
def delete_program(request):
    id = request.POST['id']
    p = shortcuts.get_object_or_404(Package, pk=id)
    msg = 'Program %s was deleted' % p.name
    p.delete()
    messages.success(request, msg)
    return http.HttpResponseRedirect(reverse('programs'))

def programs(request):
    packages = Package.objects.all()
    return shortcuts.render(request, 'index.html', {'packages': packages})

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
