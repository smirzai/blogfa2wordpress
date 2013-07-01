from django.shortcuts import render
from django.http import HttpResponseRedirect
from blgf2wrdprs.forms import ContactForm
from blgf2wrdprs.exporter.exportBlogfa27  import *
import zipfile


def compressFile(name):
   zippedFile = zipfile.ZipFile(name + ".zip", "w")
   zippedFile.write(name + ".xml")
   zippedFile.close()
 
def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            print form.cleaned_data["email"]
            siteName = form.cleaned_data["website"]
            extractSite(siteName)
            compressFile(siteName)
            
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/blogfa2wordpress/thanks') # Redirect after POST
    else:
        form = ContactForm() # An unbound form
    return render(request, 'contact.html', {
        'form': form,
    })


def thanks(request):
    return render(request, 'thanks.html')
