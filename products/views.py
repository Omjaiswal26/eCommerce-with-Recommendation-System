from django.shortcuts import render , redirect
from products.models import Product , Category
from accounts.models import Cart , CartItems
from django.http import HttpResponseRedirect

def get_product(request , slug):
    try:
        product = Product.objects.get(slug = slug)
        return render(request , 'product/product.html' , context = {'product' : product})
    
    except Exception as e:
        print(e)


def get_category(request , slug):
    try:
        cat = Category.objects.get(slug = slug)
        category_name = cat.category_name
        context  = {'products' : Product.objects.filter(category__category_name = category_name)}
        return render(request , 'categories/category.html' , context)
        
    
    except Exception as e:
        print(e)

