from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    UNIT_CHOICES = [
        ('celsius', 'Celsius (°C)'),
        ('fahrenheit', 'Fahrenheit (°F)'),
    ]
    THEME_CHOICES = [
        ('dark', 'Dark Mode'),
        ('light', 'Light Mode'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='celsius')
    theme_preference = models.CharField(max_length=10, choices=THEME_CHOICES, default='dark')
    saved_location_city = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class FavoriteCity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    city_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'city_name']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.city_name}"