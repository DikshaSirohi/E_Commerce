from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Payment

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'created', 'updated', 'get_total_items', 'get_total_price')
    list_filter = ('created',)
    search_fields = ('user__username', 'session_key')
    readonly_fields = ('created', 'updated')
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'get_total_price')
    list_filter = ('created',)
    search_fields = ('product__name', 'cart__user__username')
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'paid', 'get_total_cost', 'created')
    list_filter = ('status', 'paid', 'created')
    search_fields = ('user__username', 'email', 'first_name', 'last_name')
    readonly_fields = ('created', 'updated')
    
    def get_total_cost(self, obj):
        return obj.get_total_cost()
    get_total_cost.short_description = 'Total Cost'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity', 'get_cost')
    search_fields = ('product__name', 'order__id')
    
    def get_cost(self, obj):
        return obj.get_cost()
    get_cost.short_description = 'Cost'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'stripe_payment_intent_id', 'amount', 'status', 'created')
    list_filter = ('status', 'created')
    search_fields = ('order__id', 'stripe_payment_intent_id')
    readonly_fields = ('created', 'updated')
