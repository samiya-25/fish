from django.contrib import admin
from .models import Fish, FishCategory
from .models import Order, OrderItem

# Register your models here.
admin.site.register(Fish)
admin.site.register(FishCategory)
admin.site.register(Order)
admin.site.register(OrderItem)