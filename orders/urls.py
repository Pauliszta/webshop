from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('new/', views.new_order, name='new_order'),
    path('order-more-info/', views.order_more_info, name='order_more_info'),

]
