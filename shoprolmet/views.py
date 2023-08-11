from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required

from account.models import UserBase
from orders.models import Order, OrderItem

from .forms import ProductAddForm, ProductEditForm, OrderEditForm, CustomerEditForm
from .models import Category, Product
import datetime
from decimal import Decimal
from cart.forms import CartAddProductForm

# Create your views here.


class IndexView(View):
    """
    Displays the homepage of company's webiste
    """
    def get(self, request):
        return render(request, "index.html")


class DashboardView(View):
    """
    Displays homepage for company's employees.

    Returns divided by status quantities of orders and shows products with the smallest quantity on webshop
    """
    def get(self, request):
        today_date = datetime.datetime.now()
        products_quantity = Product.objects.count()
        today_orders = Order.objects.count()
        new_orders = Order.objects.filter(status='1').count()
        paid_order = Order.objects.filter(status='2').count()
        in_progress_orders = Order.objects.filter(status='3').count()
        ready_to_go_orders = Order.objects.filter(status='4').count()
        sent_orders = Order.objects.filter(status='5').count()
        small_stock_products = Product.objects.all().order_by('stock')[:3]
        context = {
            'date': today_date,
            'products_quantity': products_quantity,
            'small_stock_products': small_stock_products,
            'today_orders': today_orders,
            'new_orders': new_orders,
            'paid_orders': paid_order,
            'in_progress_orders': in_progress_orders,
            'ready_to_go_orders': ready_to_go_orders,
            'sent_orders': sent_orders,
        }
        return render(request, "dashboard.html", context=context)


def about_view(request):
    """
    Returns the side with information about company
    """
    return render(request, "about.html")


def offer_view(request):
    """
    Returns the side with company's offers
    """
    return render(request, "offer.html")


def contact_view(request):
    """
    Returns the side with contact
    """
    return render(request, "contact.html")


class ShopView(View):
    """
    Displays the products on webshop
    """
    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.all().filter(available=True)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        products_with_net_price = []

        for product in products:
            price_net = round(Decimal(str(product.price)) / Decimal(1.23), 2)
            products_with_net_price.append({'product': product, 'price_net': price_net})

        context = {
            'category': category,
            'categories': categories,
            'products_with_net_prices': products_with_net_price,
            'products': products,
        }
        return render(request, "shop.html", context=context)


def product_detail(request, product_id):
    """
    Displays the details about product.
    """
    product = get_object_or_404(Product, id=product_id,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop-product-details.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


class ProductsListView(View):
    """
    Returns list of all products for employees.
    Shows also non-available products.
    """
    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.all().order_by('created')
        p = Paginator(products, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        context = {
            'category': category,
            'categories': categories,
            'page_obj': page_obj,
        }
        return render(request, "products-list.html", context=context)


class ProductAddView(View):
    """
    Allows to add new product by employee
    """
    def get(self, request):
        form = ProductAddForm()
        return render(request, "product-add.html", {'form': form})

    def post(self, request):
        form = ProductAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products/list/')
        return render(request, "product-add.html", {'form': form})


@staff_member_required
def edit_product(request, product_id):
    """
    Allows edit product by employee
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductEditForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/products/list/')
    else:
        form = ProductEditForm(instance=product)
    return render(request, "product-edit.html", {'form': form,
                                                 'product': product})


class ProductView(View):
    """
    Returns details of product for employee's view
    """
    def get(self, request, product_id):
        product = get_object_or_404(Product,
                                    id=product_id)
        context = {'product': product}
        return render(request, "product-details.html", context=context)


class OrdersListView(View):
    """
    Returns list of all orders for employees.
    """
    def get(self, request):
        orders = Order.objects.all()
        p = Paginator(orders, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        context = {'page_obj': page_obj}
        return render(request, "orders-list.html", context=context)


class OrdersListPaidView(View):
    """
    Shows all paid orders.
    """
    def get(self, request):
        orders = Order.objects.filter(status='2').order_by('-created')
        p = Paginator(orders, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        context = {'page_obj': page_obj}
        return render(request, "orders-list.html", context=context)


class OrdersListPrepareView(View):
    """
    Shows all orders in preparing.
    """
    def get(self, request):
        orders = Order.objects.filter(status='3').order_by('-created')
        p = Paginator(orders, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        context = {'page_obj': page_obj}
        return render(request, "orders-list.html", context=context)


class OrdersListReadyView(View):
    """
    Shows all orders ready to go.
    """
    def get(self, request):
        orders = Order.objects.filter(status='4').order_by('-created')
        p = Paginator(orders, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        context = {'page_obj': page_obj}
        return render(request, "orders-list.html", context=context)


class OrdersListSentView(View):
    """
    Shows all order which are sent.
    """
    def get(self, request):
        orders = Order.objects.filter(status='5').order_by('-created')
        p = Paginator(orders, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        context = {'page_obj': page_obj}
        return render(request, "orders-list.html", context=context)


class OrdersListNewView(View):
    def get(self, request):
        orders = Order.objects.filter(status='1').order_by('-created')
        p = Paginator(orders, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        context = {'page_obj': page_obj}
        return render(request, "orders-list.html", context=context)

@staff_member_required
def edit_order(request, order_id):
    """
    Allows to edit the order and changes the status, when the order is in next step
    """
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderEditForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/orders/list/')
    else:
        form = OrderEditForm(instance=order)
    return render(request, "order-edit.html", {'form': form, 'order': order})


class OrderView(View):
    """
    Shows order's details
    """
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order_items = OrderItem.objects.all().filter(order=order_id)
        context = {'order': order,
                   'order_items': order_items}
        return render(request, "order-details.html", context=context)


class ClientsListView(View):
    """
    Returns list of all clients for employees.
    Shows also non-active clients.
    """
    def get(self, request):
        customers = UserBase.objects.all().filter(is_staff=False)
        p = Paginator(customers, 5)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        context = {'page_obj': page_obj}
        return render(request, "customers-list.html", context=context)


class ClientView(View):
    """
    Shows client's details
    """
    def get(self, request, customer_id):
        customer = get_object_or_404(UserBase, id=customer_id)
        orders = Order.objects.all().filter(user=customer_id)
        context = {'customer': customer,
                   'orders': orders,
                   }
        return render(request, "customer-details.html", context=context)

@staff_member_required
def edit_customer(request, customer_id):
    """
    Allows to edit the clients and can to reactive account for deleted client
    """
    customer = get_object_or_404(UserBase, id=customer_id)

    if request.method == 'POST':
        form = CustomerEditForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/customers/list/')
    else:
        form = CustomerEditForm(instance=customer)
    return render(request, "order-edit.html", {'form': form,
                                               'customer': customer})
