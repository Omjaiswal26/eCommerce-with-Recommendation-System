from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name' , 'price' , 'category' , 'sub_category']
    inlines = [ProductImageAdmin]

admin.site.register(Product , ProductAdmin)

admin.site.register(ProductImage)

admin.site.register(Coupon)