from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ghostapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'rdp.views.programs', name="programs"),
    url(r'^programs/add/$', 'rdp.views.add_program', name="add_program"),
    url(r'^programs/delete/$', 'rdp.views.delete_program', name="delete_program"),
    url(r'^programs/deploy/$', 'rdp.views.deploy_program', name="deploy_program"),

    url(r'^rds_setup/$', 'rdp.views.rds_setup', name="rds_setup"),

)
