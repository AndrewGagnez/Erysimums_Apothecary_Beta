from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

from django.contrib.auth.middleware import AuthenticationMiddleware
from shop.views import Index
from shop.views import CheckOut
from shop.views import Cart
from shop.views import OrderView

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('catalog', views.catalog, name='catalog'),
    path('cart', AuthenticationMiddleware(Cart.as_view()), name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', AuthenticationMiddleware(OrderView.as_view()), name='orders'),
    path('paypal', include('paypal.standard.ipn.urls')),
]