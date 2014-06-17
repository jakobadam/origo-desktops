from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView

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

)
