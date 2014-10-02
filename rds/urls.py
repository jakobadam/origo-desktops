from django.conf.urls import (
    patterns, url, include
    )
from django.core.urlresolvers import (reverse_lazy)

from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

from .views import (
    PackageUpdate,
    PackageCreate,
    PackageDelete
    )

urlpatterns = patterns('',

    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', RedirectView.as_view(url=reverse_lazy('setup'), permanent=True)),

    url(r'^setup/$', 'rds.views.setup', name='setup'),
    url(r'^setup/ad_external/$', 'rds.views.ad_external_setup', name='ad_external_setup'),
    url(r'^setup/ad_type/$', 'rds.views.ad_type', name='ad_type'),
    url(r'^setup/cancel/$', 'rds.views.cancel', name='cancel'),
    url(r'^setup/server/$', 'rds.views.server_setup', name='server_setup'),    
    
    url(r'^software/$', RedirectView.as_view(url=reverse_lazy('packages_local'), permanent=True),
        name='software'),
    url(r'^software/cloud/$', 'rds.views.packages_cloud', name='packages_cloud'),
    url(r'^software/cloud/deploy/$', 'rds.views.deploy_package', name='deploy_package'),
    
    url(r'^software/local/$', 'rds.views.packages_local', name='packages_local'),
    url(r'^software/local/create/$', PackageCreate.as_view(), name='add_package'),    
    url(r'^software/local/delete/(?P<pk>\d+)/$', PackageDelete.as_view(), name='delete_package'),
    url(r'^software/local/update/(?P<pk>\d+)/$', PackageUpdate.as_view(), name='update_package'),
    url(r'^software/local/deploy/$', 'rds.views.deploy_package', name='deploy_package'),

    url(r'^software/server/packages$', 'rds.views.packages', name='packages'),
    url(r'^software/server/applications/$', 'rds.views.applications', name='applications'),
    url(r'^software/server/applications/refresh/$', 'rds.views.refresh_applications', name='refresh_applications'),

    url(r'^deployment/publish/(?P<pk>\d+)/$', 'rds.views.deployment_publish', name='deployment_publish'),
    url(r'^deployment/unpublish/(?P<pk>\d+)/$', 'rds.views.deployment_unpublish', name='deployment_unpublish'),        

    url(r'^api/join/$', 'rds.views.join', name='api_join'),
    url(r'^api/server/(?P<pk>\d+)/rdp/settings.rdp', 'rds.views.rdp_settings', name='rdp_settings'),

     )
