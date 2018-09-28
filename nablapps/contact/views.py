from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            #Sende mail
            subject, message, email = contact_form.process()
            try:
                send_mail(subject, message, email, ['webkom@nabla.ntnu.no'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return HttpResponseRedirect('/contact/success/')

    else:
        if request.user.is_authenticated:
            #last in skjema uten navn og e-post
            contact_form = ContactForm(initial={'your_name': request.user.get_full_name(), 'email': request.user.email})
            context = {'contact_form': contact_form}
            return render(request, 'contact/contact.html', context)
        else:
            contact_form = ContactForm
            context = {'contact_form': contact_form,}
            return render(request, 'contact/contact.html', context)


def success(request):
    return render(request, 'contact/success.html')
# Create your views here.

