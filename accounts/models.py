from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from products.models import Product , Coupon 

class Profile(BaseModel):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name='profile')
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100 , null=True , blank=True)

    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid = False , cart__user = self.user).count()

    def __str__(self):
        return str(self.user)



class Cart(BaseModel):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='cart_user')
    coupon = models.ForeignKey(Coupon , on_delete=models.SET_NULL , null=True , blank=True )
    is_paid = models.BooleanField(default=False)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []

        for cart_item in cart_items:
            price.append(cart_item.product.price)


        return sum(price)
        
    def total(self):
        cart_items = self.cart_items.all()
        price = []

        for cart_item in cart_items:
            price.append(cart_item.product.price)

        if self.get_cart_total() > 0:
            if self.coupon:
                coupon_discount = self.coupon.discount_price
                if self.coupon.minimum_amount < sum(price):
                    return sum(price) + 60 - self.coupon.discount_price 

                self.coupon = None
                self.save()
                
            return sum(price) + 60
        return sum(price)
    
    def empty_cart(self):
        cart_items = self.cart_items.all()
        for cart_item in cart_items:
            cart_item.delete()

    def __str__(self):
        return str(self.user)
    
class   CartItems(BaseModel):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE , related_name='cart_items')
    product = models.ForeignKey(Product , on_delete=models.SET_NULL , null=True , blank=True)

    def __str__(self):
        return str(self.product.product_name)

class CustomerDetails(BaseModel):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='details')
    customer_id = models.IntegerField(null=True)
    first_name = models.CharField(max_length=100 , verbose_name="First Name")
    last_name = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200)
    pincode = models.IntegerField(null=True , blank=True)
    email = models.EmailField()
    phone = models.IntegerField()

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)

    
class Order(BaseModel):
    order_id = models.IntegerField()
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='order_user')
    name = models.CharField(max_length=100 , null=True)
    details = models.ManyToManyField(CustomerDetails , related_name='customer_details')
    order_items = models.ManyToManyField(CartItems , related_name='order_items')
    order_price = models.IntegerField(null=True)
    order_status = models.CharField(max_length=100)
    order_is_paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
            
@receiver(post_save , sender = User)
def send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            send_account_activation_email(email , email_token)
    except Exception as e:
        print(e)