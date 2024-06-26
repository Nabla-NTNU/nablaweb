from datetime import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView, View

from nablapps.accounts.models import NablaUser
from nablapps.officeBeer.models import Account
from nablapps.officeBeer.views import Transaction

from .models import Category, Order, OrderProduct, Product


class IndexView(LoginRequiredMixin, ListView):
    queryset = Product.objects.order_by("-pub_date")
    template_name = "nablashop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "nablashop/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = "nablashop/category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["products"] = self.object.product_set.order_by("-pub_date")
        return context


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product, user=request.user, ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "Antall varer ble oppdatert.")
            return redirect("nablashop:order-summary")
        else:
            order.products.add(order_product)
            messages.info(request, "Varen ble lagt til i handlevognen.")
            return redirect("nablashop:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, "Varen ble lagt til i handlevognen.")
        return redirect("nablashop:order-summary")


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product, user=request.user, ordered=False
            )[0]
            order.products.remove(order_product)
            messages.info(request, "Varen ble fjernet fra handlevognen")
            return redirect("nablashop:order-summary")
        else:
            messages.info(request, "Varen ble ikke funnet i handlevognen.")
            return redirect("nablashop:product_detail", slug=slug)
    else:
        messages.info(request, "Du har ingen aktiv ordere.")
        return redirect("nablashop:product_detail", slug=slug)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {"object": order}
            return render(self.request, "order_summary.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Du har ingen aktiv ordre")
            return redirect("/")


@login_required
def remove_single_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product, user=request.user, ordered=False
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
            messages.info(request, "Antall varer ble oppdatert.")
            return redirect("nablashop:order-summary")
        else:
            messages.info(request, "Varen ble ikke funnet i handlevognen.")
            return redirect("nablashop:product_detail", slug=slug)
    else:
        messages.info(request, "Du har ingen aktiv ordere.")
        return redirect("nablashop:product_detail", slug=slug)


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = "nablashop/purchase.html"

    def post(self, request, *args, **kwargs):
        purchase_form = PurchaseForm(request.POST)
        pose = ""

        if purchase_form.is_valid():
            loggedinUser = request.user
            user = NablaUser.objects.get_from_rfid(
                purchase_form.cleaned_data["user_card_key"]
            )
            account = Account.objects.get_or_create(user=user)[0]
            order = Order.objects.get(user=loggedinUser)

            # Should this rather be in clean form?
            if account.balance < order.get_total():
                messages.error(
                    request,
                    "Ikke nok Nabla-Coin på konto. Kunne ikke gjennomføre handel.",
                )
                return HttpResponseRedirect("/shop/")

            account.balance -= order.get_total()

            products_list = order.products
            for item in products_list.all():
                pose += str(item) + "; "
                if item.product.stock < item.quantity:
                    messages.error(
                        request,
                        f"Ikke nok {item.product} på lager. Kunne ikke gjennomføre handel.",
                    )
                    return HttpResponseRedirect("/shop/")
                item.product.stock -= item.quantity

                Product(
                    name=item.product.name,
                    description_short=item.product.description_short,
                    description=item.product.description,
                    pub_date=item.product.pub_date,
                    photo=item.product.photo,
                    price=item.product.price,
                    stock=item.product.stock,
                    category=item.product.category,
                    slug=item.product.slug,
                ).save()

                item.product.delete()

            Transaction(
                description=f"{order.get_total()} Nabla-Coin ble trukket fra {account.user.username}'s konto.",
                amount=0,
                account=account,
                date=datetime.now(),
            ).save()
            account.save()

            subject = "[NABLASHOP] Kvittering for handel"
            message = f"Du har handlet {pose} \n Vis denne kvitteringen på kontoret når du skal hente varene dine"
            email = "noreply@nabla.no"
            mailadress = f"{account.user.username}@stud.ntnu.no"
            send_mail(subject, message, email, [mailadress], fail_silently=False)

            messages.success(
                request,
                f"Gjennomført! Nabla-Coin på konto {user}: {account.balance}",
            )

            return HttpResponseRedirect("/shop/")

        context = {"form": purchase_form}

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PurchaseForm()
        context["last_transactions"] = Transaction.objects.filter(
            amount__lt=0
        ).order_by("-date")[:3]
        return context


class PurchaseForm(forms.Form):
    # product = forms.ChoiceField(widget=forms.RadioSelect)
    user_card_key = forms.IntegerField(
        label="Kortnummer",
        widget=forms.TextInput(attrs={"placeholder": "Scan kort", "autofocus": "true"}),
    )

    # todo valid product
    def clean_user_card_key(self):
        data = self.cleaned_data["user_card_key"]

        # Check that there is an account with the given card key
        if not NablaUser.objects.get_from_rfid(data):
            raise ValidationError(
                "Det er ingen registrerte kontoer med den kortnøkkelen,\
                                    brukeren har kanskje ikke registrert NTNU-kortet sitt."
            )
        return data
