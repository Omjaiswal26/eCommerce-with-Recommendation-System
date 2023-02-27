from django.urls import path
from .views import *
from .views import add_to_cart

urlpatterns = [
    path('login/' , login_page , name='login'),
    path('register/' , register_page , name='register'),
    path('logout' , logout_view , name="logout"),
    path('activate/<email_token>' , activate_email , name='activate_email'),
    path('add-to-cart/<uid>/' , add_to_cart , name="add_to_cart"),
    path('buy-now/<uid>/' , buy_now , name="buy_now"),
    path('cart/' , cart , name="cart"),
    path('remove-cart/<cart_item_uid>/' , remove_from_cart , name="remove_from_cart"),
    path('remove-coupon/<uid>/' , remove_coupon , name="remove_coupon"),
    path('details/' , details , name="details"),
    path('order/<uid>/' , order , name='order'),
    path('your_orders' , your_orders , name="your_orders"),
    path('order_detail/<order_id>/' , order_detail , name="order_detail"),
]