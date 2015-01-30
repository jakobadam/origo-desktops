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
    PackageDelete,
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

    url(r'^software/$', RedirectView.as_view(url=reverse_lazy('packages_local'), permanent=True), name='software'),
    url(r'^software/store/$', 'rds.views.packages_cloud', name='packages_cloud'),

    url(r'^software/local/$', 'rds.views.packages_local', name='packages_local'),
    url(r'^software/local/upload/$', PackageCreate.as_view(), name='add_package'),
    url(r'^software/local/delete/(?P<pk>\d+)/$', PackageDelete.as_view(), name='delete_package'),
    url(r'^software/local/update/(?P<pk>\d+)/$', PackageUpdate.as_view(), name='update_package'),
    url(r'^software/local/install/(?P<pk>\d+)/$', 'rds.views.install_package', name='install_package'),
    url(r'^software/local/uninstall/(?P<pk>\d+)/$', 'rds.views.uninstall_package', name='uninstall_package'),

    url(r'^software/server/packages$', 'rds.views.packages_server', name='packages_server'),
    url(r'^software/server/applications/$', 'rds.views.applications', name='applications'),
    url(r'^software/server/applications/refresh/$', 'rds.views.refresh_applications', name='refresh_applications'),

    url(r'^farm/$', 'rds.views.farm_list', name='farm_list'),
    url(r'^farm/(?P<pk>\d+)/$', 'rds.views.farm_show', name='farm_show'),
    url(r'^farm/(?P<farm_pk>\d+)/package/(?P<farm_package_pk>\d+)/delete/$', 'rds.views.farm_package_delete', name='farm_package_delete'),
    url(r'^farm/(?P<farm_pk>\d+)/package/(?P<farm_package_pk>\d+)/add/$', 'rds.views.farm_package_add', name='farm_package_add'),        

    url(r'^farm/deployment/', ServerList.as_view(), name='deployment'),
    url(r'^farm/deployment/publish/(?P<pk>\d+)/$', 'rds.views.deployment_publish', name='deployment_publish'),
    url(r'^farm/deployment/unpublish/(?P<pk>\d+)/$', 'rds.views.deployment_unpublish', name='deployment_unpublish'),

    url(r'^api/join/$', 'rds.views.join', name='api_join'),
    url(r'^api/server/(?P<pk>\d+)/rdp/settings.rdp', 'rds.views.rdp_settings', name='rdp_settings'),

    url(r'^api/server/create/$', ServerCreate.as_view(), name='server_create'),
)
