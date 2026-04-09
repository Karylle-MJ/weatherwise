import pytz
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from .models import UserProfile, FavoriteCity, UserActivity
from django.utils import timezone

# Remove the dashboard/header completely
admin.site.site_header = "User Management"
admin.site.site_title = "User Management"
admin.site.index_title = "Users"
admin.site.unregister(Group)

# Simple User Admin without any dashboard
class SimpleUserAdmin(UserAdmin):
    # Only show these columns
    list_display = ['username', 'email', 'is_active']
    list_filter = ['is_active']
    search_fields = ['username', 'email']
    
    # Minimal fields
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active'),
        }),
    )
    
    # Remove all actions that show extra sections
    actions = ['delete_selected']

# Register User model
admin.site.unregister(User)
admin.site.register(User, SimpleUserAdmin)

# Custom User Activity Admin - Only Login/Logout
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'formatted_datetime', 'ip_address']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['user', 'activity_type', 'details', 'ip_address', 'user_agent', 'created_at']
    date_hierarchy = 'created_at'
    
    def formatted_datetime(self, obj):
        # Convert UTC to Asia/Manila timezone
        manila_tz = pytz.timezone('Asia/Manila')
        local_time = obj.created_at.astimezone(manila_tz)
        return local_time.strftime('%B %d, %Y - %I:%M:%S %p')
    formatted_datetime.short_description = 'Date & Time (Philippines)'
    
    
    # Only show login and logout activities
    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            activity_type__in=['login', 'logout']
        )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

# Register UserProfile (readonly for admin)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme_preference', 'formatted_created_at']
    search_fields = ['user__username']
    readonly_fields = ['user', 'theme_preference', 'saved_location_city', 'created_at']
    
    def formatted_created_at(self, obj):
        return obj.created_at.strftime('%B %d, %Y - %I:%M:%S %p')
    formatted_created_at.short_description = 'Created At'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_active', 'formatted_date_joined']
    list_filter = ['is_active', 'date_joined']
    search_fields = ['username', 'email']
    
    def formatted_date_joined(self, obj):
        return obj.date_joined.strftime('%B %d, %Y - %I:%M:%S %p')
    formatted_date_joined.short_description = 'Date Joined'
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    readonly_fields = ['date_joined', 'last_login']

# Unregister default User and register custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)