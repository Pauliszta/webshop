from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('view/', views.cart_view, name='cart_view'),
    path('add/<int:product_id>', views.cart_add, name='cart_add'),
    path('delete/', views.cart_delete, name='cart_delete'),
    # path('update/', views.cart_update, name='cart_update'),

]

