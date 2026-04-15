from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    THEME_CHOICES = [
        ('dark', 'Dark Mode'),
        ('light', 'Light Mode'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    details = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'User Activities'
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.created_at}"

class UserFavoriteActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_activities')
    city_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    activity_note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'city_name']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.city_name}: {self.activity_note[:50]}"

class HeartedActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hearted_activities')
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    activity = models.CharField(max_length=200)
    detail = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'city', 'activity']
    
    def __str__(self):
        return f"{self.user.username} - {self.city}: {self.activity}"