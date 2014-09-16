from django.conf.urls import (
    patterns, url, include
    )

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

    url(r'^$', 'rds.views.setup', name="setup"),
        
    url(r'^packages/$', 'rds.views.packages', name="packages"),
    url(r'^packages/create/$', PackageCreate.as_view(), name="add_package"),    
    url(r'^packages/delete/(?P<pk>\d+)/$', PackageDelete.as_view(), name="delete_package"),
    url(r'^packages/update/(?P<pk>\d+)/$', PackageUpdate.as_view(), name='update_package'),

    url(r'^packages/deploy/$', 'rds.views.deploy_package', name="deploy_package"),

    url(r'^setup/ad_external/$', 'rds.views.ad_external_setup', name="ad_external_setup"),
    url(r'^setup/ad_internal/$', 'rds.views.ad_internal_setup', name="ad_internal_setup"),    
    url(r'^setup/ad_type/$', 'rds.views.ad_type', name='ad_type'),
    url(r'^setup/cancel/$', 'rds.views.cancel', name="cancel"),
    url(r'^setup/server/$', 'rds.views.server_setup', name="server_setup"),    
        
    url(r'^api/join/$', 'rds.views.join', name="api_join"),
    url(r'^api/server/(?P<pk>\d+)/rdp/settings.rdp', 'rds.views.rdp_settings', name='rdp_settings'),

     )
