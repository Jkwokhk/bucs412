from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(BoardGame)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Rating)