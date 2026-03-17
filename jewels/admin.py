from django.contrib import admin
from .models import CustomUser, Item, ItemImage, Cart, Order, OrderItem, Rate


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 0

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'mobile', 'is_active', 'is_staff', 'is_verified']
    list_filter = ['is_active', 'is_staff', 'is_verified']
    search_fields = ['username', 'email', 'mobile']
    list_editable = ['is_active']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_type', 'weight', 'price', 'is_active']
    list_filter = ['item_type', 'is_active']
    search_fields = ['name']
    inlines = [ItemImageInline]

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ['rate_type', 'per_gram_rate', 'date']
    list_filter = ['rate_type', 'date']

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ['user', 'item', 'quantity', 'created_at']
#     list_filter = ['created_at']
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity', 'added_at')
    list_filter = ('added_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']

