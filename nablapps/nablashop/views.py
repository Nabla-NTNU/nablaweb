from django.views.generic import DetailView, ListView

from .models import Category, Product


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
