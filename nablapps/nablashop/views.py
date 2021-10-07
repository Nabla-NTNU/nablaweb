from django.contrib import messages
from django.views.generic import DetailView, ListView, View
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Category, Product, OrderProduct, Order
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(ListView):
    queryset = Product.objects.order_by("-pub_date")
    template_name = "nablashop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "nablashop/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class CategoryDetailView(DetailView):
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
    order_product, created = OrderProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
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
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
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
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
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
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
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