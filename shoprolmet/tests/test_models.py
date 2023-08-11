from django.contrib.auth.models import User
from django.test import TestCase

from shoprolmet.models import Category, Product


class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name='test', slug='test')

    def test_category_model_entry(self):
        """
        Test Category model
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model_entry(self):
        """
        Test Category model default name
        """
        data = self.data1
        self.assertEqual(str(data), 'test')


class TestProductModel(TestCase):
    def setUp(self):
        Category.objects.create(name='test', slug='test')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1, name='django', created_by_id=1, slug='test', price='10.00',
                                            image='test', width='10')
    def test_products_model_entry(self):
        """
        Test Product model
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django')
