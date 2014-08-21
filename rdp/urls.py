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

    url(r'^$', 'rdp.views.setup', name="setup"),
        
    url(r'^packages/$', 'rdp.views.packages', name="packages"),
    url(r'^packages/create/$', PackageCreate.as_view(), name="add_package"),    
    url(r'^packages/delete/(?P<pk>\d+)/$', PackageDelete.as_view(), name="delete_package"),
    url(r'^packages/update/(?P<pk>\d+)/$', PackageUpdate.as_view(), name='update_package'),

    url(r'^packages/deploy/$', 'rdp.views.deploy_package', name="deploy_package"),
    
    url(r'^api/join/$', 'rdp.views.join', name="api_join"),
)
