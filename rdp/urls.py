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

    url(r'^setup/$', 'rdp.views.setup', name="setup"),
    url(r'^setup/rename$', 'rdp.views.rename_setup', name="rename_setup"),
    url(r'^setup/domain$', 'rdp.views.domain_setup', name="domain_setup"),
    url(r'^setup/password$', 'rdp.views.password_setup', name="password_setup"),

)
