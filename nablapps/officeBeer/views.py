from datetime import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from nablapps.accounts.models import NablaUser

from .models import Account, DepositRequest, Product, Transaction


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "officeBeer/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account"] = Account.objects.get_or_create(user=self.request.user)[0]
        context["permission_required"] = self.request.user.has_perm(
            "officeBeer.sell_product"
        )
        context["transaction_list"] = Transaction.objects.filter(
            account=context["account"], amount__lt=0
        ).order_by("-date")
        context["deposit_list"] = Transaction.objects.filter(
            account=context["account"], amount__gt=0
        ).order_by("-date")
        return context


class PurchaseForm(forms.Form):
    product = forms.ChoiceField(widget=forms.RadioSelect)
    user_card_key = forms.IntegerField(
        label="Kortnummer",
        widget=forms.TextInput(attrs={"placeholder": "Scan kort", "autofocus": "true"}),
    )

    # Could use ModelChoiceField for product, but this would require to
    # subclass ModelChoiceField to override label_from_instance method.
    # https://docs.djangoproject.com/en/2.1/ref/forms/fields/#modelchoicefield
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        product_list = [
            (p.id, f"{p.name} - {p.price}kr") for p in Product.objects.all()
        ]
        self.fields["product"].choices = product_list
        self.fields["product"].initial = product_list[0]
        self.fields["product"].widget.option_template_name = (
            "officeBeer/radio_option.html"
        )

    # todo valid product
    def clean_user_card_key(self):
        data = self.cleaned_data["user_card_key"]

        # Check that the rfid is positive
        if int(data) < 0:
            raise ValidationError("The number must be a positive integer")

        # Check that there is an account with the given card key
        if not NablaUser.objects.get_from_rfid(data):
            raise ValidationError(
                "There are no registered accounts with that card key,\
                                    the user might not have registered their key card or \
                                    does not have an account for officebeer"
            )
        return data


class DepositRequestForm(forms.Form):
    """
    Form to register when you have deposited money. The admin has to approve the request
    """

    amount = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)


class PurchaseView(PermissionRequiredMixin, TemplateView):
    template_name = "officeBeer/purchase.html"
    permission_required = "officeBeer.sell_product"

    def post(self, request, *args, **kwargs):
        purchase_form = PurchaseForm(request.POST)

        if purchase_form.is_valid():
            user = NablaUser.objects.get_from_rfid(
                purchase_form.cleaned_data["user_card_key"]
            )
            account = Account.objects.get_or_create(user=user)[0]
            product_id = purchase_form.cleaned_data["product"]
            product = Product.objects.get(id=product_id)
            price = product.price

            # Should this rather be in clean form?
            if account.balance < price:
                messages.error(request, "Not enough money on account")
                return redirect(self.request.resolver_match.view_name)

            account.balance -= price

            Transaction(
                description=f"{price}NOK from {account.user.username}'s account for {product.name}",
                amount=-price,
                account=account,
                date=datetime.now(),
            ).save()
            account.save()

            return redirect(self.request.resolver_match.view_name)

        context = {"form": purchase_form}

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PurchaseForm()
        context["last_transactions"] = Transaction.objects.filter(
            amount__lt=0
        ).order_by("-date")[:3]
        return context


class DepositRequestView(LoginRequiredMixin, TemplateView):
    """View for the user to create a depositRequest."""

    template_name = "officeBeer/deposit.html"

    def post(self, request, *args, **kwargs):
        deposit_form = DepositRequestForm(request.POST)

        if deposit_form.is_valid():
            # todo is get_or_create best solution
            account = Account.objects.get_or_create(user=request.user)[0]

            DepositRequest(
                account=account, amount=deposit_form.cleaned_data["amount"]
            ).save()
            messages.info(
                request,
                "Innskudd lagt til, pengene havner på kontoen din når kjellerstyret godkjenner den.",
            )

            return redirect(self.request.resolver_match.view_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = DepositRequestForm(user=self.request.user)
        context["deposit_requests"] = DepositRequest.objects.filter(
            account__user=self.request.user
        )  # Deposit requests awaiting approval
        return context
