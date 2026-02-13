from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:fish_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:fish_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:fish_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:fish_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout-success/', views.checkout_success, name='checkout_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('orders/', views.orders, name='orders'),

]
