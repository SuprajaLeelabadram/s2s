from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Artwork)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Customize)
