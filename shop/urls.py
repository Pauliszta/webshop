"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from shoprolmet.views import IndexView, DashboardView, AboutView, OfferView, ContactView, ShopView, ProductView, \
    ProductsListView, ProductAddView, OrderView, OrdersListView, ClientsListView, ClientView, ShopProductView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('main/', DashboardView.as_view()),
    path('about/', AboutView.as_view()),
    path('offer/', OfferView.as_view()),
    path('contact/', ContactView.as_view()),
    path('shop/', ShopView.as_view()),
    path('shop/product/<int:id>', ShopProductView.as_view()),
    path('product/<int:id>', ProductView.as_view()),
    path('products/list/', ProductsListView.as_view()),
    path('product/add/', ProductAddView.as_view()),
    # path('product/modify/<int:id>', ProductEditView.as_view()),
    path('order/<int:id>', OrderView.as_view()),
    path('orders/list/', OrdersListView.as_view()),
    # path('order/edit/', OrderEditView.as_view()),
    path('clients/list/', ClientsListView.as_view()),
    path('client/<int:id>/', ClientView.as_view()),
    # path('login/', LoginView.as_view()),
    # path('registration', Registraction.as_view()),


]
