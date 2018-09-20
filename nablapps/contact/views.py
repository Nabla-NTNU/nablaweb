from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            #Sende mail
            send_mail('Subject','melding.', 'kaprests@outlook.com' ,['kaprests@stud.ntnu.no'], fail_silently=False,)

            return HttpResponseRedirect('/contact/success/')

    else:
        contact_form = ContactForm
        context = {'contact_form': contact_form,}
        return render(request, 'contact/contact.html', context)


def success(request):
    return HttpResponse('Yes da')
# Create your views here.

