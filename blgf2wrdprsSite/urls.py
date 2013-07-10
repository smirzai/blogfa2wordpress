from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^blogfa2wordpress/', include('blgf2wrdprs.urls')),
 
)
