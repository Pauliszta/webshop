from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Category, Product


# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


class DashboardView(View):
    def get(self, request):
        return render(request, "dashboard.html")


class AboutView(View):
    def get(self, request):
        return render(request, "about.html")


class OfferView(View):
    def get(self, request):
        return render(request, "offer.html")


class ContactView(View):
    def get(self, request):
        return render(request, "contact.html")


class ShopView(View):
    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        context = {
            'category': category,
            'categories': categories,
            'products': products,
        }
        return render(request, "shop.html", context=context)


class ShopProductView(View):
    def get(self, request, id):
        product = get_object_or_404(Product,
                                    id=id,
                                    available=True)
        context = {'product': product}
        return render(request, "shop-product-details.html", context=context)


class ProductsListView(View):
    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.all()
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        context = {
            'category': category,
            'categories': categories,
            'products': products,
        }
        return render(request, "products-list.html", context=context)


class ProductAddView(View):
    def get(self, request):
        return render(request, "product-add.html")


class ProductView(View):
    def get(self, request, id):
        product = get_object_or_404(Product,
                                    id=id,
                                    available=True)
        context = {'product': product}
        return render(request, "product-details.html", context=context)


class OrdersListView(View):
    def get(self, request):
        return render(request, "orders-list.html")


class OrderView(View):
    def get(self, request):
        return render(request, "order-details.html")


class ClientsListView(View):
    def get(self, request):
        return render(request, "clients-list.html")


class ClientView(View):
    def get(self, request):
        return render(request, "client-details.html")
