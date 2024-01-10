from .models import Mailfeed, Subscription

from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import SubscribeForm, MailFeedForm, EmailForm


class MailFeedListView(PermissionRequiredMixin, ListView):
    permission_required = "Mailfeed.generate_mailfeeds"
    model = Mailfeed
    template_name = "mailfeed/mailfeed_list.html"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateMailFeedView(PermissionRequiredMixin, View):
    permission_required = "Mailfeed.generate_mailfeeds"

    def get(self, request):
        mailfeed_form = MailFeedForm()
        context = {"mailfeed_form": mailfeed_form}
        return render(request, "mailfeed/create_mailfeed.html", context)

    def post(self, request):
        mailfeed_form = MailFeedForm(request.POST)
        if mailfeed_form.is_valid():
            mailfeed_name = mailfeed_form.get_name()

            mailfeed = Mailfeed.objects.create(name=mailfeed_name)
            mailfeed.save()
        return redirect(reverse("mailfeed-list"))


class SubscribeView(View):
    def get(self, request, mailfeed_id: int):
        subscribe_form = SubscribeForm()
        context = {"subscribe_form": subscribe_form}
        mailfeed = Mailfeed.objects.get(pk=mailfeed_id)
        context["mailfeed"] = mailfeed
        return render(request, "mailfeed/subscribe_mailfeed.html", context)

    def post(self, request, mailfeed_id: int):
        mailfeed = Mailfeed.objects.get(pk=mailfeed_id)
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            email = subscribe_form.get_email()
            if Subscription.objects.filter(email=email).exists():
                return render(
                    request,
                    "mailfeed/msg.html",
                    {"msg": "Denne eposten er allerede registrert fra før."},
                )
            else:
                subscription = Subscription.objects.create(
                    mailfeed=mailfeed, email=email
                )
                subscription.save()
                return render(
                    request, "mailfeed/msg.html", {"msg": "Mailadressen registrert!"}
                )
        return render(request, "mailfeed/invalid_email.html", {"mailfeed": mailfeed})


# TODO: Lag unsubscribe view som som kan legges ved som lenke i mailen.


class MailFeedDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "Mailfeed.generate_mailfeeds"

    def get(self, request, mailfeed_id: int):
        email_form = EmailForm()
        context = {"email_form": email_form}
        mailfeed = Mailfeed.objects.get(pk=mailfeed_id)
        context["mailfeed"] = mailfeed
        email_list = mailfeed.get_email_list()
        context["email_list"] = email_list
        return render(request, "mailfeed/mailfeed_detail.html", context)

    def post(self, request, mailfeed_id: int):
        email_form = EmailForm(request.POST)
        mailfeed = Mailfeed.objects.get(pk=mailfeed_id)
        email_list = mailfeed.get_email_list()
        if not email_form.is_valid():
            return HttpResponse("Oops! Noe gikk galt.")

        subject = email_form.get_subject()
        content = email_form.get_content()
        for email in email_list:
            try:
                send_mail(
                    subject,
                    content,
                    None,
                    [email],
                    fail_silently=False,
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found")

        return redirect(reverse("mailfeed-detail", kwargs={"mailfeed_id": mailfeed_id}))
