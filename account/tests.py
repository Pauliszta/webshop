from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import UserBase
from orders.models import Order
from django.urls import reverse
from .forms import RegistrationForm

# Create your tests here.


User = get_user_model()


class UserBaseModelTest(TestCase):

    def test_email_label(self):
        user = UserBase.objects.create_user(email='test@example.com', user_name='testuser', first_name='Test',
                                     last_name='User',
                                     password='user')

        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'adres e-mail')

    def test_user_name_label(self):
        user = UserBase.objects.create_user(email='test@example.com', user_name='testuser', first_name='Test',
                                     last_name='User',
                                     password='user')

        field_label = user._meta.get_field('user_name').verbose_name
        self.assertEqual(field_label, 'user name')

    def test_first_name_max_length(self):
        user = UserBase.objects.create_user(email='test@example.com', user_name='testuser', first_name='Test',
                                     last_name='User',
                                     password='user')
        max_length = user._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_user_creation(self):
        UserBase.objects.create_user(email='test@example.com', user_name='testuser', first_name='Test',
                                     last_name='User',
                                     password='user')
        user_count = UserBase.objects.count()
        self.assertEqual(user_count, 1)

    def test_user_str_representation(self):
        user = UserBase.objects.create_user(email='test@example.com', user_name='testuser', first_name='Test',
                                            last_name='User',
                                            password='user')
        self.assertEqual(str(user), user.user_name)

    def test_user_is_not_staff_by_default(self):
        user = UserBase.objects.create_user(email='test@example.com', user_name='testuser', first_name='Test',
                                            last_name='User',
                                            password='user')
        self.assertFalse(user.is_staff)


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com', user_name='testuser', password='testpassword'
        )
        self.dashboard_url = reverse('account:dashboard')

    def test_dashboard_view_authenticated_user(self):
        self.client.login(email='test2@example.com', password='testpassword2')

        Order.objects.create(user=self.user, address2='address2', address1='address1', post_code='post_code',
                             full_name='full_name', city='city', payment_method='payment_method',
                             delivery_method='delivery_method', total_paid=10, status='5')
        Order.objects.create(user=self.user, address2='address2', address1='address1', post_code='post_code',
                             full_name='full_name', city='city', payment_method='payment_method',
                             delivery_method='delivery_method', total_paid=10, status='5')
        Order.objects.create(user=self.user, address2='address2', address1='address1', post_code='post_code',
                             full_name='full_name', city='city', payment_method='payment_method',
                             delivery_method='delivery_method', total_paid=10, status='5')

        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)

    def test_dashboard_view_unauthenticated_user(self):
        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, reverse('account:login') + '?next=' + self.dashboard_url)


class AccountRegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('account:register')

    def test_register_view_GET(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/registration/register.html')
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_register_view_POST_valid_form(self):
        user_data = {
            'email': 'test@example.com',
            'user_name': 'testuser',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, 200)

    def test_register_view_POST_invalid_form(self):
        invalid_user_data = {
            'email': 'invalidemail',
            'user_name': '',
            'password': 'short',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post(self.register_url, invalid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'Wprowadź poprawny adres email.')


class DeleteUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com', user_name='testuser', password='testpassword'
        )
        self.delete_user_url = reverse('account:delete_user')

    def test_delete_user_view_authenticated_user(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.get(self.delete_user_url)
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)

