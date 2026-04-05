from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.db.models import Count

class WeatherWiseAdminSite(AdminSite):
    site_header = 'WeatherWise Admin'
    site_title = 'WeatherWise Admin Portal'
    index_title = 'Admin Dashboard'
    
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_users'] = User.objects.count()
        extra_context['active_users'] = User.objects.filter(is_active=True).count()
        return super().index(request, extra_context=extra_context)

# Create admin site instance
weatherwise_admin = WeatherWiseAdminSite(name='weatherwise_admin')