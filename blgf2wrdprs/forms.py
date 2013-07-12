from django import forms

class ContactForm(forms.Form):
    website = forms.CharField(max_length=100)
    email = forms.EmailField()

  
