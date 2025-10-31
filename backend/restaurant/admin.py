from django.contrib import admin
from .models import Staff, Customer, Menu, Order, OrderItem

admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderItem)
