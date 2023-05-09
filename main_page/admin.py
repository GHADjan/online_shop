from django.contrib import admin
from .models import Category, Product, Cart

# Показываем в админ панели
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)





