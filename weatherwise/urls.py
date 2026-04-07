from django.urls import path
from . import views

app_name = 'weatherwise'

urlpatterns = [
    # Page views
    path('', views.home, name='home'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('profile/', views.profile_view, name='profile'),
    path('clear-history/', views.clear_search_history, name='clear_history'),
    path('save-location/', views.save_location, name='save_location'),
    
    # API endpoints
    path('api/weather/', views.weather_api, name='weather_api'),
    path('api/weather/coordinates/', views.weather_by_coordinates, name='weather_by_coordinates'),
    path('api/favorites/toggle/', views.toggle_favorite, name='toggle_favorite'),
    path('api/favorites/check/', views.check_favorite, name='check_favorite'),
    path('api/save-theme/', views.save_theme, name='save_theme'),
]