from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.admin.views.decorators import staff_member_required

from shoprolmet import views
from shoprolmet.views import IndexView, DashboardView, \
    ShopView, ProductView, ProductsListView, OrdersListView, ClientsListView, ClientView, \
    OrdersListNewView, OrdersListPaidView, \
    OrdersListPrepareView, OrdersListReadyView, OrdersListSentView, OrderView, ProductAddView
# ShopProductView,


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('main/', staff_member_required(DashboardView.as_view())),
    path('about/', views.about_view, name='about'),
    path('offer/', views.offer_view, name='offer'),
    path('contact/', views.contact_view, name='contact'),
    path('shop/', ShopView.as_view()),
    # path('shop/product/<int:product_id>/', ShopProductView.as_view()),
    path('shop/product/<int:product_id>/', views.product_detail),

    path('product/<int:product_id>/', staff_member_required(ProductView.as_view())),
    path('products/list/', staff_member_required(ProductsListView.as_view())),
    path('product/add/', staff_member_required(ProductAddView.as_view())),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),


    path('orders/list/', staff_member_required(OrdersListView.as_view())),
    path('order/<int:order_id>/', staff_member_required(OrderView.as_view())),
    path('order/edit/<int:order_id>/', views.edit_order),
    path('orders/list/new/', staff_member_required(OrdersListNewView.as_view())),
    path('orders/list/paid/', staff_member_required(OrdersListPaidView.as_view())),
    path('orders/list/prepare/', staff_member_required(OrdersListPrepareView.as_view())),
    path('orders/list/ready/', staff_member_required(OrdersListReadyView.as_view())),
    path('orders/list/sent/', staff_member_required(OrdersListSentView.as_view())),

    path('customers/list/', staff_member_required(ClientsListView.as_view())),
    path('customer/<int:customer_id>/', staff_member_required(ClientView.as_view())),
    path('customer/edit/<int:customer_id>', views.edit_customer),

    path('account/', include('account.urls', namespace='account')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('cart.urls', namespace='cart')),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
