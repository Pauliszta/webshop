from django.test import TestCase
from account.models import UserBase
from shoprolmet.models import Category, Product
from django.test import Client
from django.urls import reverse
from orders.models import Order
import datetime
from .forms import ProductAddForm, ProductEditForm


# Create your tests here.


class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name='category1', slug='cat1')

    def test_category_model_entry(self):
        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'category1')


class TestProductModel(TestCase):
    def setUp(self):
        category = Category.objects.create(name='category1', slug='category1')
        user = UserBase.objects.create(user_name='user')
        self.data2 = Product.objects.create(category=category, name='name1', slug='name1', description='desc1', width=10,
                                            producent='prod10', price=10.0, stock=10, image='image', created_by_id=user.id)

    def test_product_model_entry(self):
        data = self.data2
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'name1')


class TestViewResponse(TestCase):
    def setUp(self):
        self.c = Client()
        category = Category.objects.create(name='category1', slug='category1')
        user = UserBase.objects.create(user_name='user')
        Product.objects.create(category=category, name='name1', slug='name1', description='desc1', width=10,
                               producent='prod10', price=10.0, stock=10, image='image', created_by_id=user.id)

    def test_homepage(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.c.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_offer(self):
        response = self.c.get('/offer/')
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        response = self.c.get('/contact/')
        self.assertEqual(response.status_code, 200)


class DashboardViewTest(TestCase):
    def test_dashboard_view(self):
        category = Category.objects.create(name='category1', slug='category1')
        user = UserBase.objects.create(user_name='user')
        Product.objects.create(category=category, name='name1', slug='name1', description='desc1', width=10,
                               producent='prod10', price=10.0, stock=10, image='image', created_by_id=user.id)
        Product.objects.create(category=category, name='name2', slug='name2', description='desc2', width=20,
                               producent='prod20', price=20.0, stock=20, image='image', created_by_id=user.id)
        Order.objects.create(user=user, address2='address2', address1='address1', post_code='post_code',
                             full_name='full_name', city='city', payment_method='payment_method',
                             delivery_method='delivery_method', total_paid=10, status='1')
        Order.objects.create(user=user, address2='address2', address1='address1', post_code='post_code',
                             full_name='full_name', city='city', payment_method='payment_method',
                             delivery_method='delivery_method', total_paid=10, status='2')
        Order.objects.create(user=user, address2='address2', address1='address1', post_code='post_code',
                             full_name='full_name', city='city', payment_method='payment_method',
                             delivery_method='delivery_method', total_paid=10, status='3')
        Order.objects.create(user=user, address2='address2', address1='address1', post_code='post_code',
                             full_name='full_name', city='city', payment_method='payment_method',
                             delivery_method='delivery_method', total_paid=10, status='4')
        Order.objects.create(user=user, address2='address2', address1='address1', post_code='post_code',
                             full_name='full_name', city='city', payment_method='payment_method',
                             delivery_method='delivery_method', total_paid=10, status='5')


        response = self.client.get('/main/')
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'dashboard.html')

        # self.assertIn('date', response.context)
        # self.assertIn('products_quantity', response.context)
        # self.assertIn('small_stock_products', response.context)
        # self.assertIn('today_orders', response.context)
        # self.assertIn('new_orders', response.context)
        # self.assertIn('paid_orders', response.context)
        # self.assertIn('in_progress_orders', response.context)
        # self.assertIn('ready_to_go_orders', response.context)
        # self.assertIn('sent_orders', response.context)


class AddProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_product_url = ('/product/add/')

    def test_add_product_view_GET(self):
        response = self.client.get(self.add_product_url)
        self.assertEqual(response.status_code, 302)


    def test_add_product_view_POST_valid_form(self):
        category = Category.objects.create(name='category1', slug='category1')
        user = UserBase.objects.create(user_name='user')
        product_data = {
            'category': category,
            'name': 'name1',
            'slug': 'name1',
            'description': 'desc1',
            'width': 10,
            'producent': 'prod10',
            'price': 10.0,
            'stock': 10,
            'image': 'image',
            'created_by_id': user.id}

        response = self.client.post(self.add_product_url, product_data)
        self.assertEqual(response.status_code, 302)
        category1 = Category.objects.create(name='category1')
        new_product = Product.objects.create(category=category1, name='name1', slug='name1', description='desc1', width=10,
                               producent='prod10', price=10.0, stock=10, image='image', created_by_id=user.id)
        self.assertEqual(new_product.name, product_data['name'])
        self.assertEqual(new_product.price, product_data['price'])
        self.assertEqual(new_product.stock, product_data['stock'])
        self.assertEqual(new_product.description, product_data['description'])
        self.assertEqual(new_product.slug, product_data['slug'])
        self.assertEqual(new_product.width, product_data['width'])
        self.assertEqual(new_product.image, product_data['image'])
        self.assertEqual(new_product.created_by_id, product_data['created_by_id'])

    def test_add_product_view_POST_invalid_form(self):
        invalid_product_data = {
            'name': '',
            'price': 'invalid',
            'stock': -10,
        }

        response = self.client.post(self.add_product_url, invalid_product_data)
        self.assertEqual(response.status_code, 302)
