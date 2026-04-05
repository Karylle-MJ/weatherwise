import requests
from django.conf import settings
from datetime import datetime

class WeatherService:
    
    @staticmethod
    def get_weather_data(city):
        """Get current weather for a city"""
        if not settings.WEATHER_API_KEY or settings.WEATHER_API_KEY == 'your_openweathermap_api_key_here':
            return {'error': 'API key not configured'}
        
        params = {
            'q': city,
            'appid': settings.WEATHER_API_KEY,
            'units': 'metric'
        }
        
        try:
            response = requests.get(settings.WEATHER_API_URL, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                return {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'pressure': data['main']['pressure']
                }
            elif response.status_code == 404:
                return {'error': f"City '{city}' not found"}
            else:
                return {'error': f"API error: {data.get('message', 'Unknown')}"}
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_forecast_data(city):
        """Get 5-day forecast (3-hour intervals)"""
        if not settings.WEATHER_API_KEY:
            return {'error': 'API key not configured'}
        
        params = {
            'q': city,
            'appid': settings.WEATHER_API_KEY,
            'units': 'metric'
        }
        
        try:
            response = requests.get(settings.FORECAST_API_URL, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                # Process 3-hour intervals
                hourly_forecast = []
                for item in data['list'][:8]:
                    dt = datetime.fromtimestamp(item['dt'])
                    hourly_forecast.append({
                        'time': dt.strftime('%I:%M %p'),
                        'temp': round(item['main']['temp']),
                        'description': item['weather'][0]['description'],
                        'icon': item['weather'][0]['icon']
                    })
                
                # Group by day for daily forecast
                daily_forecast = {}
                for item in data['list']:
                    date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                    if date not in daily_forecast:
                        daily_forecast[date] = {
                            'temps': [],
                            'description': item['weather'][0]['description'],
                            'icon': item['weather'][0]['icon']
                        }
                    daily_forecast[date]['temps'].append(item['main']['temp'])
                
                daily_list = []
                for i, (date, values) in enumerate(list(daily_forecast.items())[:5]):
                    date_obj = datetime.strptime(date, '%Y-%m-%d')
                    daily_list.append({
                        'day': date_obj.strftime('%A'),
                        'day_short': date_obj.strftime('%a'),
                        'date': date_obj.strftime('%b %d'),
                        'high': round(max(values['temps'])),
                        'low': round(min(values['temps'])),
                        'description': values['description'],
                        'icon': values['icon']
                    })
                
                return {
                    'city': data['city']['name'],
                    'country': data['city']['country'],
                    'hourly': hourly_forecast,
                    'daily': daily_list
                }
            else:
                return {'error': f"Forecast error: {data.get('message', 'Unknown')}"}
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_weather_by_coordinates(lat, lon):
        """Get weather using coordinates"""
        params = {
            'lat': lat,
            'lon': lon,
            'appid': settings.WEATHER_API_KEY,
            'units': 'metric'
        }
        
        try:
            response = requests.get(settings.WEATHER_API_URL, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                return {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'pressure': data['main']['pressure']
                }
            else:
                return {'error': 'Could not get weather for your location'}
        except Exception as e:
            return {'error': str(e)}