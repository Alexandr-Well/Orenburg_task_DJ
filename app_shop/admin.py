from django.contrib import admin

from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(QuantityProduct)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    pass
