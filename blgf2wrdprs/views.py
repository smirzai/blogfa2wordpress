# -*- coding: UTF-8 -*-
 
from django.shortcuts import render
from django.http import HttpResponseRedirect
from blgf2wrdprs.forms import ContactForm
from blgf2wrdprs.exporter.exportBlogfa27  import *
from blgf2wrdprs.exporter.mailer import *
import zipfile
import datetime


def compressFile(name, siteName):
   zippedFile = zipfile.ZipFile(name + ".zip", "w")
   zippedFile.write(name + ".xml", siteName + ".xml")
   zippedFile.close()

def logUsage(siteName, email):
   with open("/tmp/httpd/usage.txt", "a") as myfile:
      myfile.write(str(datetime.datetime.now()) + ' : ' + siteName + ' : ' + email+"\n")  
 
def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            email =  form.cleaned_data["email"]
            siteName = form.cleaned_data["website"]
            fileName = "/tmp/" + siteName
            try:
               logUsage(siteName, email)
               extractSite(siteName, fileName)
            except (urllib2.HTTPError, UnicodeEncodeError):
               print "Error site cannot be read"   
               return render (request, 'error.html', { 'errorMessage': u'وبلاگ %s.blogfa.ir یافت نشد.' % siteName})
            
            compressFile(fileName, siteName)
            sendEmail(email,   fileName, siteName )
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks') # Redirect after POST
    else:
        form = ContactForm() # An unbound form
    return render(request, 'contact.html', {
        'form': form,
    })


def thanks(request):
    return render(request, 'thanks.html')
