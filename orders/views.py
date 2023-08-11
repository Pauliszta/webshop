from django.shortcuts import render

# Create your views here.

from shoprolmet.models import Product
from .models import Order, OrderItem


def new_order(request):
    """
    Creates the new order
    """
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
        full_name = request.POST.get('full_name')
        address1 = request.POST.get('add1')
        address2 = request.POST.get('add2')
        post_code = request.POST.get('post_code')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')
        delivery_method = request.POST.get('delivery_method')

        order = Order.objects.create(user=request.user, address2=address2, address1=address1, post_code=post_code,
                                     full_name=full_name, city=city, payment_method=payment_method,
                                     delivery_method=delivery_method, total_paid=total_price + shipping_cost, phone=phone)

        for product_id, item_data in cart.items():
            product = Product.objects.get(pk=product_id)
            quantity = item_data['quantity']
            unit_price = product.price
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=unit_price)
        for item in cart_items:
            product = item['product']
            quantity = item['quantity']
            product.stock -= quantity
            product.save()

        request.session['cart'] = {}
        return render(request, 'order-placed.html')

    context = {
        'cart_items': cart_items,
        'total_price': total_price + shipping_cost,
        'shipping_cost': shipping_cost,
    }
    return render(request, 'cart-details.html', context=context)


def order_more_info(request):
    """
    Returns the more needed information for teh order.
    """
    return render(request, 'order-more-info.html')



