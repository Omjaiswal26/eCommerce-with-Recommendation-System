from django.shortcuts import render
from products.models import Product , Category
from django.core.paginator import Paginator

def index(request):
    products = Product.objects.all()

    #set up pagination
    p = Paginator(Product.objects.all() , 8)
    page = request.GET.get('page')
    product_page = p.get_page(page)
    
    return render(request , 'home/index.html' , {'categories' : Category.objects.all() , 'products' : products , 'product_page' : product_page})

def about_us(request):
    return render(request , 'info/about_us.html')

def privacy_policy(request):
    return render(request , 'info/privacy_policy.html')

def cancellation_policy(request):
    return render(request , 'info/cancellation_policy.html')

def tnc(request):
    return render(request , 'info/tnc.html')

def anime(request):
    context  = {'products' : Product.objects.filter(category__category_name = 'Anime')}
    return render(request , 'categories/category.html' , context)


def marvel(request):
    context  = {'products' : Product.objects.filter(category__category_name = 'Marvel')}
    return render(request , 'categories/category.html' , context)


def dc(request):
    context  = {'products' : Product.objects.filter(category__category_name = 'DC')}
    return render(request , 'categories/category.html' , context)

def search(request):
    if request.method== 'GET':
        item = request.GET.get('search')
        result = Product.objects.filter(category__category_name__contains = str(item)) | Product.objects.filter(product_name__contains = str(item))
        context  = {'products' : result}
        return render(request , 'categories/category.html' , context)
    
