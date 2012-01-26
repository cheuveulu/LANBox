from django.conf.urls.defaults import patterns, include, url

#Include default views
from django.views.generic import DetailView, ListView
#Include server model
from cod.models import Server

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #Default view : list all servers
    url(r'^$', ListView.as_view(
        queryset=Server.objects.all(),
        )
    ),
    #View for ajax only html code for a server id
    url(r'^ajax/server/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Server,
            template_name='cod/server_list_minimal.html',
        )
    ),
    url(r'^ajax/server/(?P<pk>\d+)/(?P<action>\w+)$',
        'cod.views.server_ajax_command',
    ),
    #Detail view for a server
    url(r'^server/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Server,
        )
    ),


    # Admin 
    url(r'^admin/', include(admin.site.urls)),
)

# Serve MEDIA files for dev server
import settings
if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
                                (r'^%s(?P<path>.*)$' % _media_url,
                                serve,
                                {'document_root': settings.MEDIA_ROOT}))
    del(_media_url, serve)
