from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group

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