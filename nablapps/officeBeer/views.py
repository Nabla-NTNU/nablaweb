from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django import forms
from django.core.exceptions import ValidationError

from .models import Account, Transaction, Product
from datetime import datetime

class AccountView(TemplateView):
    template_name = "officeBeer/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Todo what if user does not have an account? Is get_or_create appropriate fix?
        context['account'] = Account.objects.get_or_create(user=self.request.user)[0]
        context['transaction_list'] = Transaction.objects.filter(account=context['account'])
        return context

class PurchaseForm(forms.Form):
    price = forms.IntegerField(widget=forms.RadioSelect)
    user_card_key = forms.CharField(label="Kortnummer")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        products = Product.objects.all()
        
        self.fields['price'].widget.choices=[(p.price, f"{p.name} - {p.price}kr") for p in products]
        
    def clean_user_card_key(self):
        data = self.cleaned_data['user_card_key']

        # Check that there is an account with the given card key
        if not Account.objects.filter(user__ntnu_card_number=data).exists():
            raise ValidationError(f'There are no registered accounts with card key {data},\
                                    the user might not have registered their key card or \
                                    does not have an account for officebeer')
        return data

class PurchaseView(TemplateView):
    template_name = "officeBeer/purchase.html"

    def post(self, request, *args, **kwargs):
        purchase_form = PurchaseForm(request.POST)
        
        if purchase_form.is_valid():
            account = Account.objects.get(user__ntnu_card_number=purchase_form.cleaned_data['user_card_key'])
            price = purchase_form.cleaned_data['price']
            account.balance -= price

            Transaction(description=f"{price}NOK from {account.user.username}'s account",
                        amount=price,
                        account=account,
                        date=datetime.now()).save()
            account.save()

            return redirect(self.request.resolver_match.view_name)
        
        context = {
            'form' : purchase_form
        }

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PurchaseForm()
        return context
