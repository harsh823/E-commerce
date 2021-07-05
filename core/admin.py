from django.contrib import admin
from .models import OrderItem,Order,Product,ShippingAddress,Customer
# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(ShippingAddress)

