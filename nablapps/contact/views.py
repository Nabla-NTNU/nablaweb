from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from .forms import FeedbackForm, ContactForm

import random

'''
The two views contact and feedback are almost identical, and one should probably rewrite them
using some class based magic. Added the second view on the train with unreliable internet, and I
just wanted to get it working.
'''
def contact(request):
    spam_check = False
    if request.method != 'POST':
        test_val = random.randint(0,20)
        context = make_contact_context(request, spam_check, test_val)
        #return HttpResponse('Halla ta kontakt med nabla her')
        return render(request, 'contact/contact.html', context)
    
    else:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            #spam check
            if contact_form.get_right_answer() == contact_form.get_answer():
                #Sends mail
                subject, message, email = contact_form.process()
                if not email:
                    email = 'forslagskasse@anonym.no'
                try:
                    if contact_form.get_reciever == 'postkom':
                        mailadress = 'forslagskasse.postkom@nabla.ntnu.no'
                    else:
                        mailadress = 'forslagskasse.styret@nabla.ntnu.no'
                    send_mail(subject, message, email, [mailadress], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found')
                return HttpResponseRedirect('/contact/success/')
            else:
                spam_check = True
                test_val = random.randint(0,20)
                context = make_contact_context(request, spam_check, test_val)
                #return HttpResponse('Halla ta kontakt med nabla her')
                return render(request, 'contact/contact.html', context)


def feedback(request):
    spam_check = False
    if request.method != 'POST':
        test_val = random.randint(0,20)
        context = make_feedback_context(request, spam_check, test_val)
        #return HttpResponse('Halla ta kontakt med nabla her')
        return render(request, 'contact/feedback.html', context)
    
    else:
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            #spam check
            if feedback_form.get_right_answer() == feedback_form.get_answer():
                #Sends mail
                subject, message, email = feedback_form.process()
                if not email:
                    email = 'forslagskasse@anonym.no'
                try:
                    if feedback_form.get_reciever == 'postkom':
                        mailadress = 'forslagskasse.postkom@nabla.ntnu.no'
                    else:
                        mailadress = 'forslagskasse.styret@nabla.ntnu.no'
                    send_mail(subject, message, email, [mailadress], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found')
                return HttpResponseRedirect('/contact/success/')
            else:
                spam_check = True
                test_val = random.randint(0,20)
                context = make_feedback_context(request, spam_check, test_val)
                #return HttpResponse('Halla ta kontakt med nabla her')
                return render(request, 'contact/feedback.html', context)


def success(request):
    return render(request, 'contact/success.html')


#######################################################################


#Not a view, returns appropriate context for feedback view
def make_contact_context(request, spam_check, test_val):
    if request.user.is_authenticated:
        #skjema uten navn og e-post
        contact_form = ContactForm(initial={'your_name': request.user.get_full_name(), 'email': request.user.email, 
'right_answer': test_val})
        context = {'contact_form': contact_form, 'spam_check': spam_check, 'test_val': test_val}
        return context
    else:
        #tomt skjema
        contact_form = ContactForm(initial={'right_answer': test_val})
        context = {'contact_form': contact_form, 'spam_check': spam_check, 'test_val': test_val}
        return context


def make_feedback_context(request, spam_check, test_val):
    if request.user.is_authenticated:
        #skjema uten navn og e-post
        feedback_form = FeedbackForm(initial={'your_name': request.user.get_full_name(), 'email': request.user.email, 
'right_answer': test_val})
        context = {'feedback_form': feedback_form, 'spam_check': spam_check, 'test_val': test_val}
        return context
    else:
        #tomt skjema
        feedback_form = FeedbackForm(initial={'right_answer': test_val})
        context = {'feedback_form': feedback_form, 'spam_check': spam_check, 'test_val': test_val}
        return context

