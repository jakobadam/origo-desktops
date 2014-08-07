from django import shortcuts
from django import http
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .forms import (
    ServerForm,
    PackageForm,
    JoinForm
    )

from .models import (
    Package,
    Server
    )

import json

PACKAGE_DIR = '/srv/samba/'

def add_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            p = Package(file=file, name=file.name)
            p.save()
            return http.HttpResponseRedirect(reverse('packages'))
    else:
        form = PackageForm()

    return shortcuts.render(request, 'add_package.html', {'form':form})

@require_http_methods(['POST'])
def delete_package(request):
    id = request.POST['id']
    p = shortcuts.get_object_or_404(Package, pk=id)
    msg = 'Package %s was deleted' % p.name
    p.delete()
    messages.success(request, msg)
    return http.HttpResponseRedirect(reverse('packages'))

def packages(request):
    packages = Package.objects.all()
    return shortcuts.render(request, 'index.html', {'packages': packages})

@require_http_methods(['POST'])
def deploy_package(request):
    id = request.POST['id']
    package = shortcuts.get_object_or_404(Package, pk=id)    
    server = Server.objects.first()

    if not server.user or not server.password:
        err = 'You must set the username and password before doing this'
        messages.error(request, err)
        return http.HttpResponseRedirect(reverse('packages'))
    
    try:
        output = package.deploy(server)
        msg = 'Deploying %s. %s' % (package,output)
        messages.info(request, msg)
    except Exception, e:
        err = 'Error deploying %s. %s' % (package,str(e))
        messages.error(request, err)
    return http.HttpResponseRedirect(reverse('packages'))

# @require_http_methods(['POST'])
# def rename_setup(request):
#     form = RenameForm(request.POST)
#     return setup(request, form=form, rename_form=form)

# @require_http_methods(['POST'])
# def domain_setup(request):
#     form = RenameForm(request.POST)
#     return setup(request, form=form, domain_form=form)

#@require_http_methods(['POST'])
# def password_setup(request):
#     form = PasswordForm(request.POST)
#     return setup(request, form=form, password_form=form)

def setup(request, **kwargs):
    server = Server.objects.first()

    if request.method == 'POST':
        form = ServerForm(data=request.POST, instance=server)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(reverse('setup'))
    else:
        form = ServerForm(instance=server)

    if server == None:
        msg = "RDS windows server hasn't reported back..."
        messages.info(request, msg)

    return shortcuts.render(request, 'setup.html', {
        'form': form
        })

def join(request):
    form = JoinForm(data=request.REQUEST)

    if not form.is_valid():
        return http.HttpResponseBadRequest(json.dumps(form.errors))

    # FIXME:!!!
    for s in Server.objects.all():
        s.delete()

    server, created = Server.objects.get_or_create(**form.cleaned_data)
    return http.HttpResponse()
