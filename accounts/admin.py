from django.contrib import admin
from .models import UserProfile, Wishlist

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'country', 'newsletter_subscribed')
    list_filter = ('newsletter_subscribed', 'country')
    search_fields = ('user__username', 'user__email', 'city')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_product_count', 'created')
    search_fields = ('user__username',)
    readonly_fields = ('created',)
