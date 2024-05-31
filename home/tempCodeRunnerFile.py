def index(request):
    products = Product.objects.all()

    #set up pagination
    p = Paginator(Product.objects.all() , 8)
    page = request.GET.get('page')
    product_page = p.get_page(page)
    print(products)
    return render(request , 'home/index.html' , {'categories' : Category.objects.all() , 'products' : products , 'product_page' : product_page})
