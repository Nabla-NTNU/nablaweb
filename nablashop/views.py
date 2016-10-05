from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def index(request):
    product_list = Product.objects.all()
    category_list = Category.objects.all()
    context = {'product_list': product_list, 'category_list': category_list}
    return render(request, 'nablashop/index.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'nablashop/product_detail.html', {'product': product})


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'nablashop/category_detail.html', {'category': category})
