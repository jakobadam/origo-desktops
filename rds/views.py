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
    JoinForm,
    ActiveDirectoryForm,
    ActiveDirectoryInternalForm
    )

from .models import (
    Package,
    Server,
    State,
    ActiveDirectory,
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
    state = State.first_or_create()

    if state.location == State.LOCATION_SERVER_WAIT:
        return shortcuts.render(request, 'server_wait.html')            

    if state.location == State.LOCATION_AD_TYPE:
        return http.HttpResponseRedirect(reverse('ad_type'))

    if state.location == State.LOCATION_AD_EXTERNAL_SETUP:
        return http.HttpResponseRedirect(reverse('ad_external_setup'))

    if state.location == State.LOCATION_AD_INTERNAL_SETUP:
        return http.HttpResponseRedirect(reverse('ad_internal_setup'))
    
    if state.location == State.LOCATION_SERVER_SETUP:
        return http.HttpResponseRedirect(reverse('server_setup'))
            
    raise Exception('TODO: Should not happen')

def server_setup(request):
    server = Server.objects.first()

    if not server:
        msg = 'There is no server in the database! Wait for it to join.'
        return http.HttpResponseBadRequest(msg)
    
    if request.method == 'POST':
        form = ServerForm(data=request.POST, instance=server)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(reverse('setup'))
    else:
        form = ServerForm(instance=server)

    return shortcuts.render(request, 'server_setup.html', {
        'form':form
    })

    
@require_http_methods(['POST'])
def cancel(request):
    state = State.first_or_create()

    for s in Server.objects.all():
        s.delete()

    # TODO: destroy virtual machines
    
    state.location = State.LOCATION_AD_TYPE
    state.save()
    return http.HttpResponseRedirect(reverse('setup'))
    
def ad_type(request):
    state = State.first_or_create()
    if request.method == 'POST':
        if request.POST.get('existing_active_directory'):
            state.existing_active_directory = True
            state.location = State.LOCATION_AD_EXTERNAL_SETUP
        else:
            state.existing_active_directory = False
            state.location = State.LOCATION_AD_INTERNAL_SETUP
        state.save()
        return http.HttpResponseRedirect(reverse('setup'))
    return shortcuts.render(request, 'ad_type.html')        

def ad_setup(request, Form, action, headline):
    """Handle external / internal AD
    """
    if request.method == 'POST':
        ad = ActiveDirectory.first_or_create()
        state = State.first_or_create()

        form = Form(request.POST, instance=ad)
        if form.is_valid():
            form.save()

            state.location = State.LOCATION_SERVER_WAIT
            state.save()

            msg = 'Updated Active Directory Information'
            messages.info(request, msg)
            return http.HttpResponseRedirect(reverse('setup'))
    else:
        form = Form()
    return shortcuts.render(request, 'ad_setup.html', {
        'form':form,
        'action':action,
        'headline':headline
        })
    
def ad_internal_setup(request):
    Form = ActiveDirectoryInternalForm
    headline = 'New AD Setup'
    action = reverse('ad_internal_setup')
    return ad_setup(request, Form, action, headline)

def ad_external_setup(request):
    Form = ActiveDirectoryForm
    headline = 'Connect with existing AD'
    action = reverse('ad_external_setup')
    return ad_setup(request, Form, action, headline)

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

    state = State.first_or_create()
    if state.location == State.LOCATION_SERVER_WAIT:
        state.location = State.LOCATION_SERVER_SETUP
        state.save()
    
    # FIXME: TODO !!!
    for s in Server.objects.all():
        s.delete()
    # FIXME: TODO !!!
    server, created = Server.objects.get_or_create(
        password='V@grant',
        user='Administrator',
        **form.cleaned_data)
    return http.HttpResponse()
