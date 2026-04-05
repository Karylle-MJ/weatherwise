from django.db import models
from django.contrib.auth.models import User

class WeatherSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    temperature = models.FloatField()
    feels_like = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=10, blank=True)
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    pressure = models.IntegerField(null=True, blank=True)
    searched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-searched_at']
        indexes = [
            models.Index(fields=['user', '-searched_at']),
            models.Index(fields=['city']),
        ]
    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.city}: {self.temperature}°C"