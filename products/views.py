from django.shortcuts import render , redirect
from products.models import Product , Category, Rating
from accounts.models import Cart , CartItems
from django.http import HttpResponseRedirect
from .recommendation import get_recommendations, get_top_n_recommendations

def get_product(request , slug):
    try:
        product = Product.objects.get(slug = slug)
        ratings = Rating.objects.filter(product_id = product.uid)

        user_id = request.user.id
        # Generate recommendations using the collaborative filtering model
        algo, rating_df = get_recommendations()
        recommendations = get_top_n_recommendations(user_id, algo, rating_df, n=4)
        print("Recommendations: ", recommendations)
        # Retrieve the recommended product objects from the database
        recommended_products = Product.objects.filter(uid__in=recommendations)
        print(recommended_products)

        return render(request , 'product/product.html' , context = {'product' : product , 'ratings': ratings, 'recommended_products': recommended_products})
    
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

