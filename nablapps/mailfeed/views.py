from .models import MailFeed, Subscription

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
    permission_required = "mailfeed.generate_feed"
    model = MailFeed
    template_name = "mailfeed/mailfeed_list.html"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateMailFeedView(PermissionRequiredMixin, View):
    permission_required = "mailfeed.generate_feed"

    def get(self, request):
        mailfeed_form = MailFeedForm()
        context = {"mailfeed_form": mailfeed_form}
        return render(request, "mailfeed/create_mailfeed.html", context)

    def post(self, request):
        mailfeed_form = MailFeedForm(request.POST)
        if mailfeed_form.is_valid():
            mailfeed_name = mailfeed_form.get_name()

            mailfeed = MailFeed.objects.create(name=mailfeed_name)
            mailfeed.save()
        return redirect(reverse("mailfeed-list"))


class SubscribeView(View):
    def get(self, request, mailfeed_id):
        subscribe_form = SubscribeForm()
        context = {"subscribe_form": subscribe_form}
        mailfeed = MailFeed.objects.get(pk=mailfeed_id)
        context["mailfeed"] = mailfeed
        return render(request, "mailfeed/subscribe_mailfeed.html", context)

    def post(self, request, mailfeed_id):
        mailfeed = MailFeed.objects.get(pk=mailfeed_id)
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            email = subscribe_form.get_email()
            subscription = Subscription.objects.create(mailfeed=mailfeed, email=email)
            subscription.save()
            return HttpResponse("Mailadresse registrert!")
        # TODO Det ser ut som ved ugyldig epostadresse kommer vi her. Utdyp feilmeldingen.
        return HttpResponse("Noe gikk galt! Prøv igjen senere.")


class MailFeedDetailView(DetailView, PermissionRequiredMixin):
    permission_required = "mailfeed.generate_feed"

    def get(self, request, mailfeed_id):
        email_form = EmailForm()
        context = {"email_form": email_form}
        mailfeed = MailFeed.objects.get(pk=mailfeed_id)
        context["mailfeed"] = mailfeed
        email_list = mailfeed.get_email_list()
        context["email_list"] = email_list
        return render(request, "mailfeed/mailfeed_detail.html", context)

    def post(self, request, mailfeed_id):
        email_form = EmailForm(request.POST)
        mailfeed = MailFeed.objects.get(pk=mailfeed_id)
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
