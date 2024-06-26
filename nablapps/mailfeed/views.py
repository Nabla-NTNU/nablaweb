from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import EmailForm, MailFeedForm, SubscribeForm, UnsubscribeForm
from .models import Mailfeed, Subscription


class MailFeedListView(PermissionRequiredMixin, ListView):
    """An overview of all mailfeeeds"""

    permission_required = "mailfeed.generate_mailfeeds"
    model = Mailfeed
    template_name = "mailfeed/mailfeed_list.html"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateMailFeedView(PermissionRequiredMixin, View):
    """Create a new mailfeed"""

    permission_required = "mailfeed.generate_mailfeeds"

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
    """Subscribe to a mailfeed by submitting an email adress"""

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


class UnsubscribeView(View):
    """Unsubscribe from a mailfeed"""

    def get(self, request, mailfeed_id: int, uuid: str):
        unsubscribe_form = UnsubscribeForm()
        context = {"unsubscribe_form": unsubscribe_form}
        mailfeed = Mailfeed.objects.get(pk=mailfeed_id)
        subscription = Subscription.objects.filter(mailfeed=mailfeed, uuid=uuid).first()
        if subscription is None:
            return render(request, "404.html")
        context["mailfeed"] = mailfeed
        return render(request, "mailfeed/unsubscribe_mailfeed.html", context)

    def post(self, request, mailfeed_id: int, uuid: str):
        mailfeed = Mailfeed.objects.get(pk=mailfeed_id)
        subscription = Subscription.objects.filter(
            mailfeed=mailfeed, uuid=uuid
        ).first()  # Should only be one instance

        if subscription is None:
            return render(
                request,
                "mailfeed/msg.html",
                {"msg": f"Denne mailadressen abonnerer ikke på {mailfeed.name}"},
            )

        unsubscribe_form = UnsubscribeForm(request.POST)
        if unsubscribe_form.is_valid():
            result = unsubscribe_form.get_result()
            if result:
                subscription.delete()
                return render(
                    request,
                    "mailfeed/msg.html",
                    {
                        "msg": f"{subscription.email} har sluttet å abonnere på {mailfeed.name}"
                    },
                )
            else:
                redirect(
                    reverse(
                        "unsubscribe-mailfeed",
                        kwargs={"mailfeed_id": mailfeed_id, "uuid": uuid},
                    )
                )
        return render(request, "mailfeed/msg.html", {"msg": "Noe gikk galt!"})


class MailFeedDetailView(PermissionRequiredMixin, DetailView):
    """Create and send emails to a mailfeed"""

    permission_required = "mailfeed.generate_mailfeeds"

    def get(self, request, mailfeed_id: int):
        email_form = EmailForm()
        context = {"email_form": email_form}
        mailfeed = Mailfeed.objects.get(pk=mailfeed_id)
        context["mailfeed"] = mailfeed
        email_list = mailfeed.get_email_list()
        context["email_list"] = email_list
        return render(request, "mailfeed/mailfeed_detail.html", context)

    def post(self, request: HttpRequest, mailfeed_id: int):
        email_form = EmailForm(request.POST)
        mailfeed = Mailfeed.objects.get(pk=mailfeed_id)
        email_list = mailfeed.get_email_list()

        if not email_form.is_valid():
            return HttpResponse("Oops! Noe gikk galt.")

        subject = email_form.get_subject()
        for email in email_list:
            subscription = Subscription.objects.filter(
                mailfeed=mailfeed, email=email
            ).first()
            if subscription is None:
                return HttpResponse("Noe gikk galt. Prøv igjen senere.")
            content = email_form.get_content()
            content += (
                f"\n\nHvis du vil slutte å abonnere på disse mailene trykk her:\n"
            )
            unsubscribe_url = "https://nabla.no" + reverse(
                "unsubscribe-mailfeed",
                kwargs={"mailfeed_id": mailfeed_id, "uuid": subscription.uuid},
            )
            content += unsubscribe_url
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
