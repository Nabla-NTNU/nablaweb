from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm

import random

def contact(request):
    spam_check = False
    if request.method != 'POST':
        test_val = request.session['test_val'] = random.randint(0,20)
        context = make_context(request, spam_check, test_val)
        return render(request, 'contact/contact.html', context)
    
    else:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            #spam check
            if request.session['test_val'] == contact_form.get_answer():
                #Sends mail
                subject, message, email = contact_form.process()
                try:
                    send_mail(subject, message, email, ['webkom@nabla.ntnu.no'], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found')
                return HttpResponseRedirect('/contact/success/')
            else:
                spam_check = True
                test_val = ContactForm.test_val = random.randint(0,20)
                context = make_context(request, spam_check, test_val)
                return render(request, 'contact/contact.html', context)
 
        

def success(request):
    return render(request, 'contact/success.html')
# Create your views here.

#######################################################################

#Not a view, returns appropriate context for contact view
def make_context(request, spam_check, test_val):
    if request.user.is_authenticated:
        #skjema uten navn og e-post
        contact_form = ContactForm(initial={'your_name': request.user.get_full_name(), 'email': request.user.email})
        context = {'contact_form': contact_form, 'spam_check': spam_check, 'test_val': test_val}
        return context
    else:
        #tomt skjema
        contact_form = ContactForm
        context = {'contact_form': contact_form, 'spam_check': spam_check, 'test_val': test_val}
        return context

