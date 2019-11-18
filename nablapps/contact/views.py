from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from .forms import FeedbackForm, ContactForm

import random


def contact(request):
    spam_check = False
    if request.method != 'POST':
        test_val = random.randint(0,20)
        context = make_contact_context(request, spam_check, test_val)
        return render(request, 'contact/contact.html', context)
    else:
        contact_form = ContactForm(request.POST)
        
        if contact_form.is_valid():
            #spam check
            if contact_form.get_right_answer() == contact_form.get_answer():
                #Sends mail
                subject, message, email = contact_form.process()
                if not email:
                    email = 'noreply@anonym.nabla.no'
                try:
                    if contact_form.get_reciever() == 'PostKom':
                        mailadress = 'forslagskasse.postkom@nabla.ntnu.no'
                    elif contact_form.get_reciever() == 'ITV ved IFY':
                        mailadress = 'fysikk@sr-nv.no'
                    elif contact_form.get_reciever() == 'ITV ved IMF':
                        mailadress = 'imf@sr-ie.no'
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
                return render(request, 'contact/contact.html', context)


def feedback(request, template = 'feedback.html', send_to="webkom@nabla.ntnu.no"):
    spam_check = False
    if request.method != 'POST':
        test_val = random.randint(0,20)
        context = make_feedback_context(request, spam_check, test_val)
        return render(request, 'contact/' + template, context)
    else:
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            #spam check
            if feedback_form.get_right_answer() == feedback_form.get_answer():
                #Sends mail
                subject, message, email = feedback_form.process()
                try:
                    send_mail(subject, message, email, [send_to], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found')
                return HttpResponseRedirect('/contact/success/')
            else:
                spam_check = True
                test_val = random.randint(0,20)
                context = make_feedback_context(request, spam_check, test_val)
                return render(request, 'contact/' + template, context)


def success(request):
    return render(request, 'contact/success.html')


#######################################################################


# The two functions below are not views, they return appropriate context for feedback and contact view
def make_contact_context(request, spam_check, test_val):
    board_emails = (
                    ('Hele styret', 'nabla'),
                    ('Leder', 'leder'),
                    ('Nestleder', 'nestleder'),
                    ('Faddersjef/sekretær', 'sekretaer'),
                    ('Kasserer', 'kasserer'),
                    ('Bedkomsjef', 'bedriftskontakt'),
                    ('Arrangementsjef', 'arrsjef'),
                    ('Kjellersjef', 'kjellersjef'),
                    ('Ambassadør', 'ambassador'),
                    ('Websjef', 'websjef'),
                    ('Redaktør', 'redaktor'),
                )
    nabla_pos_emails = (
                    ('Alle gruppeledere', 'gruppeledere'),
                    ('Leder av ProKom', 'leder.prokom'),
                    ('Leder av QuizKom', 'quizkom'),
                    ('Leder av Koreolis', 'koreolis.kraften'),
                    ('Leder av Reka', 'reka'),
                    ('Leder av Reven', 'reven'),
                    ('Leder av Skråttcast', 'skraattcast'),
                    ('Leder av Gravitones', 'leder.gravitones'),
                    ('Leder av the Stokes', 'lederstokes'),
                    ('Musikalsk leder - Maxwells Muntre Musikanter', 'maxwells.muntre'),
                    ('Økonomiansvarlig i bedriftskontakten', 'bnokonomi'),
                    ('Revysjef', 'revy'),
                    ('Bryggemester', 'bryggemester'),
                )
    group_emails = (
                    ('PostKom', 'postkom'),
                    ('Arrkom', 'arrkom'),
                    ('BN - Bedriftkontakten Nabla', 'bedkom'),
                    ('Educom', 'educom'),
                    ('ProKom', 'prokom'),
                    ('Redaksjonen', 'nabladet'),
                    ('WebKom', 'webkom'),
                    ('Excom17', 'ekskom2019'),
                    ('Excom18', 'excom18'),
                    ('Koreolis', 'koreolis'),
                    ('nablarevyen', 'revy-alle'),
                    ('the Gravitones', 'gravitones'),
                    ('the Stokes', 'thestokes'),
                    ('utfluks', 'utfluks'),
                    ('Kjellersamarbeidet (Nabla, HC, Janus)', 'kjellern.hk18'),
                )


    if request.user.is_authenticated:
        #skjema uten navn og e-post
        contact_form = ContactForm(
                    initial={
                    'your_name': request.user.get_full_name(), 
                    'email': request.user.email, 
                    'right_answer': test_val})
        context = {'contact_form': contact_form, 
                    'spam_check': spam_check, 
                    'test_val': test_val}
        context['board_emails'] = board_emails
        context['nabla_pos_emails'] = nabla_pos_emails
        context['group_emails'] = group_emails
        return context
    else:
        #tomt skjema
        contact_form = ContactForm(initial={'right_answer': test_val})
        context = {'contact_form': contact_form, 
                    'spam_check': spam_check, 
                    'test_val': test_val}
        context['board_emails'] = board_emails
        context['nabla_pos_emails'] = nabla_pos_emails
        context['group_emails'] = group_emails
        return context


def make_feedback_context(request, spam_check, test_val):
    if request.user.is_authenticated:
        #skjema uten navn og e-post
        feedback_form = FeedbackForm(initial={
                    'your_name': request.user.get_full_name(), 
                    'email': request.user.email, 
                    'right_answer': test_val})
        context = {'feedback_form': feedback_form, 
                    'spam_check': spam_check, 
                    'test_val': test_val}
        return context
    else:
        #tomt skjema
        feedback_form = FeedbackForm(initial={'right_answer': test_val})
        context = {'feedback_form': feedback_form, 
                    'spam_check': spam_check, 
                    'test_val': test_val}
        return context

