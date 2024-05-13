from django.urls import path
from products.views import *

urlpatterns = [
    path('<slug>/' , get_product , name = 'get_product'),
    path('category/<slug>/' , get_category , name = 'get_category'),
]