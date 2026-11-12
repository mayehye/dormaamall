from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from accounts.models import UserProfile
from .models import Category, Location, ItemListing, ListingImage

# Inline UserProfile inside Django's User Admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Seller Verification Status'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_verified', 'is_staff')
    
    def get_verified(self, obj):
        return hasattr(obj, 'profile') and obj.profile.is_verified
    get_verified.boolean = True
    get_verified.short_description = 'Verified Seller'

# Unregister default User admin and register the customized one safely
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 3

@admin.register(ItemListing)
class ItemListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'location', 'price', 'status', 'is_featured', 'created_at')
    list_editable = ('status', 'is_featured')
    list_filter = ('status', 'is_featured', 'category', 'condition', 'location')
    search_fields = ('title', 'description', 'phone_number', 'seller__username')
    inlines = [ListingImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ('name',)