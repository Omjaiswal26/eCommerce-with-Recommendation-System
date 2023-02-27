from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Cart)

class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['product' , 'cart']
admin.site.register(CartItems,CartItemsAdmin)

class CustomerDetailsAdmin(admin.ModelAdmin):
    list_display = ['first_name' , 'last_name' , 'email' , 'phone']
admin.site.register(CustomerDetails,CustomerDetailsAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id' , 'name' , 'order_price' , 'order_is_paid' ,'order_status']
admin.site.register(Order,OrderAdmin)
