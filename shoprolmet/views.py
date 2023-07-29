from typing import List

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Category, Product
import datetime


# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


class DashboardView(View):
    def get(self, request):
        today_date = datetime.datetime.now()
        products_quantity = Product.objects.count()
        # today_orders_quantity =
        # last_product_added = Product.objects.all().order_by('-created')
        # last_product = last_product_added[:1]
        context = {
            'date': today_date,
            'products_quantity': products_quantity,
            # 'last_product': last_product,
        }
        return render(request, "dashboard.html", context=context)


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
    def get(self, request, product_id):
        product = get_object_or_404(Product,
                                    id=product_id,
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
    def get(self, request, product_id):
        product = get_object_or_404(Product,
                                    id=product_id,
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


def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        cart = request.session.get('cart', {})
        cart_item = cart.get(str(product_id), {'quantity': 0})
        quantity = cart_item['quantity'] + 1

        if quantity <= product.stock:
            cart_item['quantity'] = quantity
            cart[str(product_id)] = cart_item
            request.session['cart'] = cart
        else:
            error_message = f" Przekroczono dostępną ilość produktu '{product.name} {product.description}. " \
                            f"Maksymalna dostępna ilość to {product.stock}"
            return render(request, 'error_message.html', {'error_message': error_message})

    return redirect('/cart/')


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, item_data in cart.items():
        product = Product.objects.get(pk=product_id)
        quantity = item_data['quantity']
        price = product.price * quantity
        total_price += price
        cart_items.append({'product': product, 'quantity': quantity, 'price': price})
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart-details.html', context=context)


def remove_cart(request):
    if request.method == 'POST':
        request.session.pop('cart', None)
    return redirect('/cart/')


def update_cart(request):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        for product_id, quantity in request.POST.items():
            if product_id.startswith('quantity_'):
                product_id = product_id.split('_')[1]
                product = get_object_or_404(Product, pk=product_id)
                new_quantity = int(quantity)

                if new_quantity > 0 and new_quantity <= product.stock:
                    cart_item = cart.get(product_id, {'quantity': 0})
                    cart_item['quantity'] = new_quantity
                    cart[str(product_id)] = cart_item
        request.session['cart'] = cart
    return redirect('/cart/')

