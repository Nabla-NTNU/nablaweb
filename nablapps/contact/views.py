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
        contact_form = ContactForm
        context = {'contact_form': contact_form,}
        return render(request, 'contact/contact.html', context)


def success(request):
    return HttpResponse('Yes da')
# Create your views here.

