from django.contrib import admin
from .models import FishCategory, Fish, Order, OrderItem
import csv
from django.http import HttpResponse


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


def export_orders_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    
    # header row
    writer.writerow([
        'Order ID',
        'Customer',
        'Phone',
        'City',
        'Payment Method',
        'Total Amount',
        'Created At'
    ])

    for order in queryset:
        writer.writerow([
            order.id,
            order.full_name,
            order.phone,
            order.city,
            order.payment_method,
            order.total_amount,
            order.created_at
        ])

    return response

export_orders_csv.short_description = "Export selected orders to CSV"



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'city', 'payment_method', 'total_amount', 'created_at')
    actions = [export_orders_csv]


class FishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')


admin.site.register(FishCategory)
admin.site.register(Fish, FishAdmin)
