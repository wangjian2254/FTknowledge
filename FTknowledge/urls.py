from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from FTknowledge import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'knowledge.views.index'),
    url(r'^TK.html$', 'knowledge.views.index'),
    url(r'^ft/', include('knowledge.urls')),
    url(r'^tax/', include('taxcreate.urls')),
    url(r'^log/', include('model_history.urls')),
    url(r'^weixin/', include('weixin.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('', url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),  )
