from django.contrib import admin
from .models import Order, OrderItem, CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user','product', 'quantity',  'get_total_price')
    readonly_fields = ('get_total_price',)
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'unit_price', 'quantity')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product_name', 'unit_price', 'quantity')
    can_delete = False
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'created_at')
    readonly_fields = ('total', 'created_at', 'updated_at')
    inlines = (OrderItemInline,)
