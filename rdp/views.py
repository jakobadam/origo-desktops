from django import shortcuts
from django import http
from django.core.urlresolvers import (reverse, reverse_lazy)
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView
    )

from .forms import (
    ServerForm,
    PackageForm,
    JoinForm
    )

from .models import (
    Package,
    Server
    )

from winexe.exceptions import RequestException

import json

PACKAGE_DIR = '/srv/samba/'

def packages(request):
    packages = Package.objects.all()
    return shortcuts.render(request, 'package_list.html', {'packages': packages})

class PackageEdit(object):
    model = Package
    template_name = 'package_form.html'
    form_class = PackageForm
    success_url = reverse_lazy('packages')

    def form_valid(self, form):
        file_updated = self.request.FILES.get('file')
        self.object = form.save(commit=False)

        if bool(file_updated):
            self.object.file_updated()

        self.object.save()
        return http.HttpResponseRedirect(self.success_url)
    
class PackageUpdate(PackageEdit, UpdateView):
    pass

class PackageCreate(PackageEdit, CreateView):
    pass

class PackageDelete(PackageEdit, DeleteView):
    pass
    
# def add_package(request):
#     if request.method == 'POST':
#         form = PackageForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             args = form.cleaned_data.get('args')
#             p = Package(file=file, name=file.name, args=args)
#             p.save()
#             return http.HttpResponseRedirect(reverse('packages'))
#     else:
#         form = PackageForm()

#     return shortcuts.render(request, 'package_form.html', {'form':form})

@require_http_methods(['POST'])
def delete_package(request):
    id = request.POST['id']
    package = shortcuts.get_object_or_404(Package, pk=id)
    server = Server.objects.first()

    try:
        package.delete(server)
        msg = 'Package %s was deleted' % package.name
        messages.info(request, msg)
    except RequestException, e:
        err = 'Error deleting %s. %s' % (package,str(e))
        messages.error(request, err)
        return http.HttpResponseRedirect(reverse('packages'))

    messages.success(request, msg)
    return http.HttpResponseRedirect(reverse('packages'))

@require_http_methods(['POST'])
def deploy_package(request):
    id = request.POST['id']
    package = shortcuts.get_object_or_404(Package, pk=id)    
    server = Server.objects.first()

    if not server or not server.user or not server.password:
        err = 'You must set the username and password before doing this'
        messages.error(request, err)
        return http.HttpResponseRedirect(reverse('packages'))

    success = package.deploy(server)
    if success:
        messages.info(request, package.message)
    else:
        messages.error(request, package.message)
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
    if server == None:
        return shortcuts.render(request, 'setup_waiting.html')
    
    if request.method == 'POST':
        form = ServerForm(data=request.POST, instance=server)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(reverse('setup'))
    else:
        form = ServerForm(instance=server)

    return shortcuts.render(request, 'setup.html', {
        'form': form
        })

def rdp_settings(request, pk):
    server = shortcuts.get_object_or_404(Server, pk=pk)
    content_type = 'application/rdp; charset=utf-8'
    response = shortcuts.render(request, 'connect.rdp', {
        'server': server
        }, content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=settings.rdp'
    return response
    
def join(request):
    form = JoinForm(data=request.REQUEST)

    if not form.is_valid():
        return http.HttpResponseBadRequest(json.dumps(form.errors))

    # FIXME:!!!
    for s in Server.objects.all():
        s.delete()

    server, created = Server.objects.get_or_create(user='Administrator', **form.cleaned_data)
    return http.HttpResponse()
