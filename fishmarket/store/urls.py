from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('login/', views.login_view, name='login'),
    path('add-to-cart/<int:fish_id>/', views.add_to_cart, name='add_to_cart'),
]
