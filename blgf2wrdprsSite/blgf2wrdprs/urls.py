from django.conf.urls import patterns, url

from blgf2wrdprs import views
from blgf2wrdprs.views import  contact

urlpatterns = patterns('',
    url(r'^contact$',  contact)
)
