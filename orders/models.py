from django.db import models
from django.conf import settings
from shoprolmet.models import Product

# Create your models here.


class Order(models.Model):
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    full_name = models.CharField(max_length=150)
    # email = models.EmailField(max_length=100)
    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, null=True)
    post_code = models.CharField(max_length=20)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(default="1", choices=STATUES)
    billing_status = models.BooleanField(default=False)
    payment_method = models.CharField(choices=PAYMENT)
    delivery_method = models.CharField(choices=DELIVERY)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.product.name)

    def get_cost(self):
        return self.price * self.quantity
