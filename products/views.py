from django.shortcuts import render , redirect
from products.models import Product 
from accounts.models import Cart , CartItems
from django.http import HttpResponseRedirect

def get_product(request , slug):
    try:
        product = Product.objects.get(slug = slug)
        return render(request , 'product/product.html' , context = {'product' : product})
    
    except Exception as e:
        print(e)


