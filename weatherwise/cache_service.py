from django.core.cache import cache
from django.conf import settings
import requests
import json

class CacheService:
    """Cache API responses to reduce external calls"""
    
    CACHE_TIMEOUT = 600  # 10 minutes
    
    @staticmethod
    def get_weather_with_cache(city):
        """Get weather data from cache or API"""
        cache_key = f"weather_{city.lower()}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return json.loads(cached_data)
        
        # Fetch from API
        from .weather_service import WeatherService
        data = WeatherService.get_weather_data(city)
        
        if data and 'error' not in data:
            cache.set(cache_key, json.dumps(data), CacheService.CACHE_TIMEOUT)
        
        return data
    
    @staticmethod
    def get_forecast_with_cache(city):
        """Get forecast data from cache or API"""
        cache_key = f"forecast_{city.lower()}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return json.loads(cached_data)
        
        from .weather_service import WeatherService
        data = WeatherService.get_forecast_data(city)
        
        if data and 'error' not in data:
            cache.set(cache_key, json.dumps(data), CacheService.CACHE_TIMEOUT)
        
        return data