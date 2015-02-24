import logging
import json

from django import shortcuts
from django import http
from django.core.urlresolvers import (reverse, reverse_lazy)
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from django.views.generic import (
    ListView
    )

from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView
    )

from . import forms
from rds.forms import (
    ServerForm,
    PackageForm,
    ActiveDirectoryForm,
    ActiveDirectoryInternalForm
    )

from rds.models import (
    Farm,
    Package,
    Server,
    ServerRole,
    State,
    Application,
    ActiveDirectory,
    )

from rds import tasks

from async_messages.models import Message

log = logging.getLogger(__name__)

PACKAGE_DIR = '/srv/samba/'

class PackageEdit(object):
    model = Package
    template_name = 'package_form.html'
    form_class = PackageForm
    success_url = reverse_lazy('package_list')

    def form_valid(self, form):
        file_updated = self.request.FILES.get('file')
        self.object = form.save(commit=False)
        self.object.save(file_updated=file_updated)
        return http.HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form), status=422)

class PackageUpdate(PackageEdit, UpdateView):
    pass

def package_list(request):
    packages = Package.objects.all()
    return shortcuts.render(request, 'package_list.html', {
        'packages': packages
    })

def package_create(request):
    status = 200
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save(file_updated=True)
            messages.success(request, u'{} uploaded'.format(instance))
            url = reverse('package_list')
            if request.is_ajax():
                return http.JsonResponse({'location': url})
            else:
                return http.HttpResponseRedirect(url)
        else:
            if request.is_ajax():
                # trigger ajax error handler
                status = 422
    else:
        form = PackageForm()

    return shortcuts.render(request, 'software_upload_form.html', {
        'form':form
    }, status=status)

class PackageCreate(PackageEdit, CreateView):
    pass

class PackageDelete(PackageEdit, DeleteView):
    pass

@require_http_methods(['POST'])
def package_delete(request, pk):
    package = shortcuts.get_object_or_404(Package, pk=pk)
    package.delete()
    messages.info(request, 'Deleted {}'.format(package))
    return http.HttpResponseRedirect(reverse('package_list'))

class ServerCreate(CreateView):
    model = Server
    form_class = ServerForm
    template_name = 'server_form.html'
    success_url = reverse_lazy('package_list')

    # def get_form_kwargs(self):
    #     kwargs = super(ServerCreate, self).get_form_kwargs()
    #     if self.request.method == 'POST':
    #         kwargs.update({
    #             'data': self.request.REQUEST
    #             })
    #     return kwargs

class ServerList(ListView):
    model = Server
    template_name = 'server_list.html'
    
@require_http_methods(['POST'])
def package_install(request, pk=None):
    """
    TODO: take the server to install on as a query arg
    """
    package = shortcuts.get_object_or_404(Package, pk=pk)
    server = Server.objects.filter(roles__icontains='session_host').first()

    if not server or not server.user or not server.password:
        err = 'You must set the username and password before doing this'
        messages.error(request, err)
        return http.HttpResponseRedirect(reverse('package_list'))

    package.install(server)
    msg = u'Installing {} on {}'.format(package, server)
    log.info(msg)
    messages.info(request, msg)
    return http.HttpResponseRedirect(reverse('package_list'))

@require_http_methods(['POST'])
def package_uninstall(request, pk=None):
    package = shortcuts.get_object_or_404(Package, pk=pk)
    server = Server.objects.first()

    if not server or not server.user or not server.password:
        err = 'You must set the username and password before doing this'
        messages.error(request, err)
        return http.HttpResponseRedirect(reverse('package_list'))

    package.uninstall(server)

    messages.info(request, 'Un-installing {} from {}'.format(package, server))
    return http.HttpResponseRedirect(reverse('package_list'))

def setup(request, **kwargs):
    state = State.first_or_create()

    if state.location == State.LOCATION_AD_TYPE:
        return http.HttpResponseRedirect(reverse('ad_type'))

    if state.location == State.LOCATION_AD_EXTERNAL_SETUP:
        return http.HttpResponseRedirect(reverse('ad_external_setup'))

    if state.location == State.LOCATION_SERVER_WAIT:
        return shortcuts.render(request, 'server_wait.html')

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
            return http.HttpResponseRedirect(reverse('software'))
    else:
        form = ServerForm(instance=server)

    return shortcuts.render(request, 'server_setup.html', {
        'form':form
    })

@require_http_methods(['POST'])
def cancel(request):
    state = State.first_or_create()

    # for s in Server.objects.all():
    #     # Get AD server and delete it
    #     s.delete()

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
            state.location = State.LOCATION_SERVER_WAIT
        state.save()
        return http.HttpResponseRedirect(reverse('setup'))
    return shortcuts.render(request, 'ad_type.html')

def ad_external_setup(request):
    # from django.http import HttpResponse
    # from django.template import RequestContext, loader

    if request.method == 'POST':

        # There is one and only one AD
        ad = ActiveDirectory.first_or_create()
        state = State.first_or_create()

        form = ActiveDirectoryForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()

            state.location = State.LOCATION_SERVER_WAIT
            state.save()

            msg = 'Updated Active Directory Information'
            messages.info(request, msg)
            return http.HttpResponseRedirect(reverse('setup'))
    else:
        form = ActiveDirectoryForm()

    return shortcuts.render(request, 'ad_setup.html', {
        'form':form
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
    """
    TODO: Instead use a regular server form to create add the
    RDS broker
    """
    form = ServerForm(data=request.REQUEST)

    if not form.is_valid():
        return http.HttpResponseBadRequest(json.dumps(form.errors))

    state = State.first_or_create()
    if state.location == State.LOCATION_SERVER_WAIT:
        state.location = State.LOCATION_SERVER_SETUP
        state.save()

    server, created = Server.objects.get_or_create(
        **form.cleaned_data)

    Message.success('Windows server "{}" started'.format(server))
    return http.HttpResponse()

def software_cloud(request):
    return shortcuts.render(request, 'software_store.html', {
    })

def server_package_list(request):
    packages = Package.objects.filter(installed=True)
    server = Server.objects.first()
    return shortcuts.render(request, 'software_installed.html', {
        'packages': packages,
        'server': server
    })

def _handle_winrm_exception(e, request):
    from winrm.exceptions import (
        WinRMTransportError,
        UnauthorizedError
        )
    error = e.__class__
    if error == WinRMTransportError:
        messages.error(request, 'RDS Server is not responding: {}'.format(e))
    elif error == UnauthorizedError:
        url = reverse('setup')
        messages.error(request, 'Unauthorized to access RDS Server: {} \
Please update the credentials in <a href="{}">Setup</a> '.format(e, url))
    else:
        messages.error(request, str(e))

@require_http_methods(['POST'])
def deployment_publish(request, pk):
    app = shortcuts.get_object_or_404(Application, pk=pk)
    # publish
    app.publish()
    messages.success(request, "Published '{}' to RDS".format(app))
    return http.HttpResponseRedirect(reverse('applications'))

@require_http_methods(['POST'])
def deployment_unpublish(request, pk):
    app = shortcuts.get_object_or_404(Application, pk=pk)
    # un-publish
    app.unpublish()
    messages.success(request, "Un-published '{}' to RDS".format(app))
    return http.HttpResponseRedirect(reverse('applications'))

def applications_refresh(request):
    server = Server.objects.first()
    server.updated = True
    server.save()
    return http.HttpResponseRedirect(reverse('applications'))

def applications(request):
    server = Server.objects.first()
    if server.updated:
        tasks.fetch_applications.delay(server.pk)
        messages.info(request, 'Updating application list... Please refresh page')
    return shortcuts.render(request, 'application_list.html', {
        'applications':Application.objects.all(),
        'server':server
    })

def farm_list(request):
    farms = Farm.objects.all()
    return shortcuts.render(request, 'farm_list.html', {
        'farms': farms
    })

def farm_show(request, pk):
    farm = shortcuts.get_object_or_404(Farm, pk=pk)
    farms = Farm.objects.all()

    return shortcuts.render(request, 'farm_show.html', {
        'farm': farm,
        'farms': farms
    })

def farm_clone(request, pk):
    farm = shortcuts.get_object_or_404(Farm, pk=pk)

    if request.method == 'POST':
        form = forms.FarmCloneForm(request.POST)
        if form.is_valid():
            new_farm = farm.clone(form.cleaned_data['name'])
            messages.success(request, '{} created'.format(new_farm))
            return http.HttpResponseRedirect(reverse('farm_list'))

    else:
        form = forms.FarmCloneForm()

    return shortcuts.render(request, 'farm_clone_form.html', {
        'form': form,
        'farm': farm,
        'farms': Farm.objects.all()
    })

@require_http_methods(['POST'])
def farm_delete(request, pk):
    farm = shortcuts.get_object_or_404(Farm, pk=pk)
    farm.delete()
    messages.success(request, '{} deleted'.format(farm))
    return http.HttpResponseRedirect(reverse('farm_list'))

@require_http_methods(['POST'])
def farm_package_create(request, farm_pk, farm_package_pk):
    farm = shortcuts.get_object_or_404(Farm, pk=farm_pk)

    qs = farm.farm_packages.filter(pk=farm_package_pk)
    farm_package = shortcuts.get_object_or_404(qs)

    return shortcuts.render(request, 'farm_show.html', {
        'farm': farm,
        'farms': Farm.objects.all()
    })

@require_http_methods(['POST'])
def farm_package_delete(request, farm_pk, farm_package_pk):
    farm = shortcuts.get_object_or_404(Farm, pk=farm_pk)

    qs = farm.farm_packages.filter(pk=farm_package_pk)
    farm_package = shortcuts.get_object_or_404(qs)

    farm_package.delete()
    messages.info(request, 'Deleted {}'.format(farm_package, farm))

    url = reverse('farm_software', kwargs={'pk': farm.pk})
    return http.HttpResponseRedirect(url)

def farm_setup(request, pk):
    farm = shortcuts.get_object_or_404(Farm, pk=pk)
    
    queryset = farm.servers.filter(roles__icontains=ServerRole.RDS_AD)
    ad = shortcuts.get_object_or_404(queryset)

    form = ActiveDirectoryForm(instance=ad)

    return shortcuts.render(request, 'farm_existing_ad_setup_form.html', {
        'farms': Farm.objects.all(),
        'farm':farm,
        'form':form
    })

    # if request.method == 'POST':
    #     form = ServerForm(data=request.POST, instance=server)
    #     if form.is_valid():
    #         form.save()
    #         return http.HttpResponseRedirect(reverse('software'))
    # else:
    # form = ServerForm(instance=server)
    # return shortcuts.render(request, 'server_setup.html', {
    #     'form':form
    # })

def farm_deployment(request, pk):
    farm = shortcuts.get_object_or_404(Farm, pk=pk)

    return shortcuts.render(request, 'farm_deployment.html', {
        'farm':farm,
        'farms': Farm.objects.all()
    })

def farm_software(request, pk):
    farm = shortcuts.get_object_or_404(Farm, pk=pk)

    return shortcuts.render(request, 'farm_software.html', {
        'farm': farm,
        'farms': Farm.objects.all()
    })
