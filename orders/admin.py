from django.contrib import admin

from .models import Order, OrderItem

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'status', 'payment_method', 'delivery_method', 'billing_status', 'created', 'updated']
    list_filter = ['status', 'created', 'updated']
    list_editable = ['billing_status']


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'price']


admin.site.register(OrderItem, OrderItemAdmin)
