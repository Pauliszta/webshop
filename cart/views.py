from django.shortcuts import get_object_or_404, render, redirect

from cart.models import CartItem, Cart
from orders.models import Order, OrderItem
from shoprolmet.models import Product
# from .cart import Cart

# Create your views here.


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    shipping_cost = int(20)

    for product_id, item_data in cart.items():
        product = Product.objects.get(pk=product_id)
        quantity = item_data['quantity']
        price = product.price * quantity
        total_price += price
        cart_items.append({'product': product, 'quantity': quantity, 'price': price})

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        updated_cart = {}
        for product_id, item_data in cart.items():
            new_quantity = int(request.POST.get(f'quantity_{product_id}', item_data['quantity']))
            if 0 < new_quantity <= product.stock:
                item_data['quantity'] = new_quantity
            updated_cart[product_id] = item_data
        request.session['cart'] = updated_cart
        return redirect('/view/')

    context = {
        'cart_items': cart_items,
        'total_price': total_price + shipping_cost,
        'shipping_cost': shipping_cost,
    }
    return render(request, 'cart-details.html', context=context)


def cart_add(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        cart = request.session.get('cart', {})
        user = request.user
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

        return redirect('/view/')


def cart_delete(request):
    if request.method == 'POST':
        request.session.pop('cart', None)
    return redirect('/view/')


# def cart_update(request):
#     if request.method == "POST":
#         cart = request.session.get('cart', {})
#         new_quantity = 0
#         for product_id, item_data in cart.items():
#             if 0 < new_quantity <= product.stock:
#                 cart_item = cart.get(product_id, {'quantity': 0})
#                 cart_item['quantity'] = new_quantity
#                 cart[str(product_id)] = cart_item
#                 request.session['cart'] = cart
#             return redirect('/view/')

#     if request.method == 'POST':
#         cart = request.session.get('cart', {})
#         updated_cart = {}
#         for product_id, item_data in cart.items():
#             new_quantity = int(request.POST.get(f'quantity_{product_id}', item_data['quantity']))
#             if 0 < new_quantity <= product.stock:
#                 item_data['quantity'] = new_quantity
#             updated_cart[product_id] = item_data
#         request.session['cart'] = updated_cart
#         return redirect('/view/')


