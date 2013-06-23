from django.shortcuts import render
from django.http import HttpResponseRedirect
from blgf2wrdprs.forms import ContactForm

def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            print form.cleaned_data["email"]
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form
    return render(request, 'contact.html', {
        'form': form,
    })
