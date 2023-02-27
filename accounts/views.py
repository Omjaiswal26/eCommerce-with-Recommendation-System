from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from accounts.models import *
import random

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request , 'Account not found')
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request , 'Your Account is not verified')
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username = email , password = password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        else:
            messages.warning(request , 'Invalid Email Id or Password')
            return HttpResponseRedirect(request.path_info)
        
    return render(request , 'accounts/login.html')

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request , 'Account with this Email already exists')
            return HttpResponseRedirect(request.path_info)
        user_obj = User.objects.create(first_name=first_name , last_name=last_name , email=email , username=email)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request , 'An Email has been sent on your mail')
    return render(request , 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/accounts/login')
    except Exception as e:
        return HttpResponseRedirect('Invalid Email token')

@login_required
def add_to_cart(request , uid):
    product = Product.objects.get(uid = uid)
    user = request.user
    cart , _ = Cart.objects.get_or_create(user = user , is_paid = False)

    cart_items= CartItems.objects.create(cart = cart , product = product)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request , cart_item_uid):
    try:
        cart_item =CartItems.objects.get(uid = cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def buy_now(request,uid):
    product = Product.objects.get(uid = uid)
    user = request.user
    cart , _ = Cart.objects.get_or_create(user = user , is_paid = False)
    cart.empty_cart()
    
    cart_items= CartItems.objects.create(cart = cart , product = product)
    return redirect('cart')

@login_required
def cart(request):
    cart_items = CartItems.objects.filter(cart__is_paid=False , cart__user = request.user)
    cart_obj = Cart.objects.get(is_paid = False , user = request.user)
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)

        if not coupon_obj.exists():
            messages.warning(request , "Invalid Coupon")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj.coupon :
            messages.warning(request , "Coupon already applied")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.warning(request , "You must buy 10 posters to avail!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj[0].is_expired:
            messages.warning(request , "Coupon expired")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request , "Coupon applied")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
    
    context = {'cart_items': cart_items , 'cart' : cart_obj}
    return render(request , 'accounts/cart.html' , context)

def remove_coupon(request , uid):
    cart = Cart.objects.get(uid = uid)
    cart.coupon = None
    cart.save()
    messages.success(request , "Coupon Removed")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def details(request):
    cart_obj = Cart.objects.get(is_paid = False , user = request.user)
    context = {'cart' : cart_obj}

    if request.method == "POST":
        user = request.user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address_line1 = request.POST['address_line1']
        address_line2 = request.POST['address_line2']
        pincode = request.POST['pincode']
        email = request.POST['email']
        phone = request.POST['phone']
        
        pincode_list = []
        for i in range(110001,110111):
            pincode_list.append(i)

        for i in range(1,110):
            if pincode == str(pincode_list[i]):
                customer = CustomerDetails(user = user , first_name=first_name , last_name = last_name , address_line1 = address_line1 , address_line2=address_line2 , pincode = pincode , email = email , phone = phone)
                customer.save()
                uid = customer.uid
                cart_obj = Cart.objects.get(is_paid = False , user = request.user)
                cart_items = CartItems.objects.filter(cart__is_paid=False , cart__user = request.user)
                customer_detail = CustomerDetails.objects.filter(uid=uid)
                context = {'customer' : customer_detail , 'cart' : cart_obj , 'cart_items' : cart_items}
                return render(request , 'accounts/summary.html' , context)
        messages.warning(request , "Sorry , We don't deliver at that pincode yet")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request , 'accounts/details.html' , context)

def order(request , uid):
    order_id = random.randint(111111 , 999999)
    user = request.user
    details = CustomerDetails.objects.filter(uid=uid)
    cart_items = CartItems.objects.filter(cart__is_paid=False , cart__user = request.user)
    
    name = str(details[0].first_name) + ' ' + str(details[0].last_name)
    status = "Ordered"
    is_paid = False
    cart = Cart.objects.get(user=user)
    price = cart.total()

    order = Order(order_id = order_id , user = user , name=name , order_status = status , order_is_paid = is_paid , order_price = price)
    order.save()
    order.details.set(details)
    cart_items = CartItems.objects.filter(cart__is_paid=False , cart__user = request.user)
    for item in cart_items:
        print(item)
        cart_item = item
        order.order_items.add(cart_item)
        order.save()
    
    cart.empty_cart()
    return redirect('index')

@login_required
def your_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    context = {'orders' : orders}
    return render(request , 'accounts/your_orders.html' , context)


def order_detail(request,order_id):
    user = request.user
    order = Order.objects.filter(order_id=order_id)
    details = order[0].details.all()
    cart_obj = Cart.objects.get(is_paid = False , user = request.user)
    cart_items = CartItems.objects.filter(cart__is_paid=False , cart__user = request.user)
    context = {'order' : order[0] , 'customer':details , 'cart_items':cart_items , 'cart':cart_obj}
    return render(request , 'accounts/order_detail.html' , context)