import os
import sys

sys.path.append('/var/www/apps')
print "111"
print sys.version
os.environ['PYTHON_EGG_CACHE'] = '/var/www/apps/.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'blgf2wrdprsSite.settings'
sys.path.append('/var/www/apps')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
