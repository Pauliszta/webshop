from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    # path('update/', views.cart_update, name='cart_update'),
    path('view/', views.cart_detail, name='cart_details'),
    path('add/<int:product_id>', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>', views.cart_remove, name='cart_remove'),

]

