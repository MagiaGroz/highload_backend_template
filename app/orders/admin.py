from django.contrib import admin

from .models import Product, Category, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'price',
                    'status', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
