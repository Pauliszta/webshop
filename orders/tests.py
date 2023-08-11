from django.test import TestCase, RequestFactory
from django.urls import reverse


from account.models import UserBase
from shoprolmet.models import Category
from .models import Product, Order, OrderItem
from .views import new_order, order_more_info

# Create your tests here.


class OrderViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


    def test_new_order_view_POST(self):
        user = UserBase.objects.create_user(user_name='testuser', email='test@user.com', password='testpassword')
        category = Category.objects.create(name='category1', slug='category1')
        product = Product.objects.create(category=category, name='name1', slug='name1', description='desc1', width=10,
                               producent='prod10', price=10.0, stock=10, image='image', created_by_id=user.id)

        request = self.factory.post(reverse('orders:new_order'), data={
            'full_name': 'John Doe',
            'add1': '123 Main St',
            'post_code': '12345',
            'city': 'City',
            'phone': '123-456-7890',
            'payment_method': 'paypal',
            'delivery_method': 'standard',
        })
        request.user = user
        request.session = {'cart': {str(product.id): {'quantity': 1}}}

        response = new_order(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.user, user)

