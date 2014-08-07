from django.conf.urls import (
    patterns, url, include
    )

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'rdp.views.packages', name="packages"),
    url(r'^packages/add/$', 'rdp.views.add_package', name="add_package"),
    url(r'^packages/delete/$', 'rdp.views.delete_package', name="delete_package"),
    url(r'^packages/deploy/$', 'rdp.views.deploy_package', name="deploy_package"),

    url(r'^setup/$', 'rdp.views.setup', name="setup"),

    url(r'^api/join/$', 'rdp.views.join', name="api_join"),
)
