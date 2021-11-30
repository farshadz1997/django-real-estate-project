from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .forms import ContactForm
from .models import Contact
from django.contrib import messages

def ContactView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data['name']
            new_email = form.cleaned_data['email']
            new_subject = form.cleaned_data['subject']
            new_message = form.cleaned_data['message']
            
            new_contact = Contact(name=new_name, email=new_email, subject=new_subject, message=new_message)
            new_contact.save()
            messages.success(request, f'Your message has been sent successfully.')
            return HttpResponseRedirect(reverse("contact"))
        
    return render(request, 'contact.html')
