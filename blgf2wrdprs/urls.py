from django.conf.urls import patterns, url

from blgf2wrdprs import views
from blgf2wrdprs.views import  contact
from blgf2wrdprs.views import thanks

urlpatterns = patterns('',
    url(r'^contact$',  contact),
    url(r'^thanks$', thanks)
)
