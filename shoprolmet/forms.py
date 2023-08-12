from django import forms

from account.models import UserBase
from .models import Product
from orders.models import Order


class ProductAddForm(forms.ModelForm):
    name = forms.CharField(label="Nazwa produktu", min_length=4, max_length=50)
    # category = forms.CharField(label="Kategoria")
    # image = forms.ImageField(label="Zdjęcie")
    description = forms.CharField(label="Model")
    width = forms.IntegerField(label="Szerokość")
    producent = forms.CharField(label="Producenta")
    price = forms.DecimalField(label="Cena")
    stock = forms.IntegerField(label="Stan magazynowy")
    available = forms.BooleanField(label="Dostępny")
    # created_by = forms.CharField(label="Osoba zakładająca")

    class Meta:
        model = Product
        fields = ['name', 'category', 'image', 'description',
                  'width', 'producent', 'price', 'stock',
                  'available', 'created_by']


class ProductEditForm(forms.ModelForm):
    name = forms.CharField(label="Nazwa produktu", min_length=4, max_length=50)
    # category = forms.ChoiceField(label="Kategoria", choices=CATEGORY)
    description = forms.CharField(label="Model")
    width = forms.IntegerField(label="Szerokość")
    producent = forms.CharField(label="Producenta")
    price = forms.FloatField(label="Cena")
    stock = forms.IntegerField(label="Stan magazynowy")
    available = forms.BooleanField(label="Dostępny")

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'width', 'producent',
                  'price', 'stock', 'available']


DELIVERY = (
    ('1', "Poczta Polska"),
    ('2', "Kurier"),
    ('3', 'INPOST'),
)
PAYMENT = (
    ('1', "przelew"),
    ('2', "za pobraniem"),
)
STATUES = (
    ('1', 'nowe'),
    ('2', 'opłacone'),
    ('3', 'w trakcie przygotowania'),
    ('4', 'gotowe do wysłania'),
    ('5', 'wysłane'),
    ('6', 'zakończone'),
)


class OrderEditForm(forms.ModelForm):
    full_name = forms.CharField(label="Imię i nazwisko")
    address1 = forms.CharField(label="Adres1")
    address2 = forms.CharField(label="Adres2", required=False)
    city = forms.CharField(label="Miasto")
    phone = forms.CharField(label="Telefon", required=False)
    post_code = forms.CharField(label="Kod pocztowy")
    status = forms.ChoiceField(label="Status", choices=STATUES)
    billing_status = forms.BooleanField(
        label="Status płatności")
    payment_method = forms.ChoiceField(label="Metoda płatności",
                                       choices=PAYMENT)
    delivery_method = forms.ChoiceField(label="Metoda dostawy",
                                        choices=DELIVERY)

    class Meta:
        model = Order
        fields = ['full_name', 'address1', 'address2', 'city', 'phone',
                  'post_code', 'status', 'billing_status', 'payment_method',
                  'delivery_method']


class CustomerEditForm(forms.ModelForm):
    email = forms.EmailField(label='Email nie może być zmieniony',
                             max_length=100,
                             widget=forms.TextInput(
                                 attrs={'class': 'forms-control mb-3',
                                        'placeholder': 'email',
                                        'id': 'form-email',
                                        'readonly': 'readonly'}))
    user_name = forms.CharField(label='Nazwa użytkownika',
                                min_length=4,
                                max_length=50,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control mb-3',
                                        'placeholder': 'Nazwa użytkownika',
                                        'id': 'form-username',
                                        'readonly': 'readonly'}))
    first_name = forms.CharField(label='Imię', min_length=3, max_length=50,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control mb-3',
                                        'placeholder': 'Imię',
                                        'id': 'form-firstname'}))
    last_name = forms.CharField(label="Nazwisko", min_length=3, max_length=50,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control mb-3',
                                        'placeholder': 'Nazwisko',
                                        'id': 'form-lastname'}))
    address = forms.CharField(label="Adres", max_length=150,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control mb-3',
                                        'placeholder': 'Adres',
                                        'id': 'form-address'}))
    postal_code = forms.CharField(label="Kod pocztowy", max_length=20,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control mb-3',
                                            'placeholder': 'Kod pocztowy',
                                            'id': 'form-postalcode'}))
    city = forms.CharField(label="Miasto", max_length=150,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control mb-3',
                                      'placeholder': 'Miasto',
                                      'id': 'form-city'}))
    is_active = forms.BooleanField(label="Aktywny:")

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'first_name', 'last_name', 'address',
                  'postal_code', 'city', 'is_active')
