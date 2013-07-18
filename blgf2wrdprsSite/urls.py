from django.conf.urls import patterns, include, url
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('blgf2wrdprs.urls')),
(
        r'^static/(?P<path>.*)$',
            'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}
        )
)
