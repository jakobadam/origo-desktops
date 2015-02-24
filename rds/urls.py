from django.conf.urls import (
    patterns, url, include
    )
from django.core.urlresolvers import (reverse_lazy)
from django.views.generic.base import RedirectView

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from .views import (
    PackageUpdate,
    PackageCreate,
    ServerCreate,
    ServerList
    )

urlpatterns = patterns('',

    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', RedirectView.as_view(url=reverse_lazy('setup'), permanent=True)),

    url(r'^setup/$', 'rds.views.setup', name='setup'),
    url(r'^setup/ad/external/$', 'rds.views.ad_external_setup', name='ad_external_setup'),
    url(r'^setup/ad/type/$', 'rds.views.ad_type', name='ad_type'),
    url(r'^setup/cancel/$', 'rds.views.cancel', name='cancel'),
    url(r'^setup/server/$', 'rds.views.server_setup', name='server_setup'),

    url(r'^software/$', RedirectView.as_view(url=reverse_lazy('package_list'), permanent=True), name='software'),
    url(r'^software/store/$', 'rds.views.software_cloud', name='software_cloud'),

    url(r'^software/local/$', 'rds.views.package_list', name='package_list'),
    url(r'^software/local/upload/$', PackageCreate.as_view(), name='package_create'),
    url(r'^software/local/delete/(?P<pk>\d+)/$', 'rds.views.package_delete', name='package_delete'),
    url(r'^software/local/update/(?P<pk>\d+)/$', PackageUpdate.as_view(), name='package_update'),
    url(r'^software/local/install/(?P<pk>\d+)/$', 'rds.views.package_install', name='package_install'),
    url(r'^software/local/uninstall/(?P<pk>\d+)/$', 'rds.views.package_uninstall', name='package_uninstall'),

    url(r'^software/server/packages$', 'rds.views.server_package_list', name='server_package_list'),
    url(r'^software/server/applications/$', 'rds.views.applications', name='applications'),
    url(r'^software/server/applications/refresh/$', 'rds.views.applications_refresh', name='applications_refresh'),

    url(r'^farms/$', 'rds.views.farm_list', name='farm_list'),
    url(r'^farm/(?P<pk>\d+)/$', 'rds.views.farm_show', name='farm_show'),
    url(r'^farm/(?P<pk>\d+)/clone/$', 'rds.views.farm_clone', name='farm_clone'),
    url(r'^farm/(?P<pk>\d+)/delete/$', 'rds.views.farm_delete', name='farm_delete'),
    url(r'^farm/(?P<pk>\d+)/deployment/$', 'rds.views.farm_deployment', name='farm_deployment'),
    url(r'^farm/(?P<pk>\d+)/software/$', 'rds.views.farm_software', name='farm_software'),
    url(r'^farm/(?P<pk>\d+)/setup/$', 'rds.views.farm_setup', name='farm_setup'),

    url(r'^farm/(?P<farm_pk>\d+)/package/(?P<farm_package_pk>\d+)/delete/$', 'rds.views.farm_package_delete', name='farm_package_delete'),
    url(r'^farm/(?P<farm_pk>\d+)/package/(?P<farm_package_pk>\d+)/create/$', 'rds.views.farm_package_create', name='farm_package_create'),        

    url(r'^farm/deployment/', ServerList.as_view(), name='deployment'),
    url(r'^farm/deployment/publish/(?P<pk>\d+)/$', 'rds.views.deployment_publish', name='deployment_publish'),
    url(r'^farm/deployment/unpublish/(?P<pk>\d+)/$', 'rds.views.deployment_unpublish', name='deployment_unpublish'),
    

    url(r'^api/join/$', 'rds.views.join', name='api_join'),
    url(r'^api/server/(?P<pk>\d+)/rdp/settings.rdp', 'rds.views.rdp_settings', name='rdp_settings'),

    url(r'^api/server/create/$', ServerCreate.as_view(), name='server_create'),
)
