from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , null=True , blank=True)
    category_image = models.ImageField(upload_to="categories")
    category_top = models.BooleanField(null=True)

    def save(self , *args , **kwargs):
        self.slug = slugify(self.category_name)
        super(Category , self).save(*args,**kwargs)

    def __str__(self) -> str:
        return self.category_name

class SubCategory(BaseModel):
    subcategory_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , null=True , blank=True)

    def save(self , *args , **kwargs):
        self.slug = slugify(self.subcategory_name)
        super(SubCategory , self).save(*args,**kwargs)

    def __str__(self) -> str:
        return self.subcategory_name

class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , null=True , blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , related_name="products_category")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE , related_name="products_sub_category" , null=True)
    price = models.IntegerField()
    product_description = models.TextField()

    def save(self , *args , **kwargs):
        self.slug = slugify(self.product_name)
        super(Product , self).save(*args,**kwargs)

    def __str__(self) -> str:
        return self.product_name

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name="product_images")
    image = models.ImageField(upload_to="product")


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)