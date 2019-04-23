from django.contrib import admin
from .models import Product, Contact, Feature_Product, Order, OrderUpdate, UserProfile

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)
admin.site.register(UserProfile)
admin.site.register(Feature_Product)
