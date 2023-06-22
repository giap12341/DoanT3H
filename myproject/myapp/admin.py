from django.contrib import admin
from .models import Product,Category,Profile
# Register your models here.
# ******************************************** PRODUCT *********************************************
@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ['id','name']
@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','category']
@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['id','user','name']