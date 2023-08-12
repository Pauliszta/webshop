from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shoprolmet.models import Product
from .cart import Cart

from .forms import CartAddProductForm


def cart_detail(request):
    """
    Displays the shopping cart's view and adding the shipping cost to the order.
    """
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    shipping_cost = int(20)
    is_cart_empty = not cart

    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    if request.method == 'POST':
        for product_id, item_data in cart.items():
            updated_quantity = int(request.POST.get(f'quantity_{product_id}', item_data['quantity']))
            if 0 < updated_quantity <= products.get(id=product_id).stock:
                cart_item = cart.get(product_id)
                cart_item['quantity'] = updated_quantity
                request.session.modified = True

    for product_id, item_data in cart.items():
        product = None
        quantity = item_data['quantity']
        price = 0
        total = 0

        for p in products:
            if str(p.id) == product_id:
                product = p
                price = product.price
                total = price * quantity

        if product:
            price = product.price
            total_price += price * quantity
            cart_items.append({'product': product, 'quantity': quantity, 'price': price, 'total': total})

    context = {
        'cart_items': cart_items,
        'total_price': total_price + shipping_cost,
        'shipping_cost': shipping_cost,
        'is_cart_empty': is_cart_empty,
    }
    return render(request, 'cart-details.html', context=context)

@require_POST
def cart_add(request, product_id):
    """
    Adds product to the shopping cart.

    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('/view/')


def cart_remove(request, product_id):
    """
    Deletes the shopping cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('/view/')

