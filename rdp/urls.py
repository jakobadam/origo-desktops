from django.conf.urls import patterns, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'rdp.views.programs', name="programs"),
    url(r'^programs/add/$', 'rdp.views.add_program', name="add_program"),
    url(r'^programs/delete/$', 'rdp.views.delete_program', name="delete_program"),
    url(r'^programs/deploy/$', 'rdp.views.deploy_program', name="deploy_program"),

    url(r'^setup/$', 'rdp.views.setup', name="setup"),

    url(r'^api/join/$', 'rdp.views.join', name="api_join"),
)
