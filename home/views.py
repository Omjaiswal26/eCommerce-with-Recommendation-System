from django.shortcuts import render
from products.models import Product

def index(request):
    context  = {'products' : Product.objects.all()}
    return render(request , 'home/index.html' , context)

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
    
