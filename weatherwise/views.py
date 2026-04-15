import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import WeatherSearch
from .weather_service import WeatherService
from .activity_service import ActivityService
from accounts.models import UserProfile, FavoriteCity, UserFavoriteActivity, HeartedActivity
from .cache_service import CacheService

# ==================== PAGE VIEWS ====================

@login_required
def home(request):
    weather_data = None
    forecast_data = None
    suggestions = None
    city_searched = request.GET.get('city')
    
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if city_searched:
        weather_data = WeatherService.get_weather_data(city_searched)
        if weather_data and 'error' not in weather_data:
            WeatherSearch.objects.create(
                user=request.user,
                city=weather_data['city'],
                country=weather_data['country'],
                temperature=weather_data['temperature'],
                feels_like=weather_data['feels_like'],
                description=weather_data['description'],
                icon=weather_data['icon'],
                humidity=weather_data['humidity'],
                wind_speed=weather_data['wind_speed'],
                pressure=weather_data['pressure']
            )
            suggestions = ActivityService.get_suggestions(
                weather_data['description'],
                weather_data['temperature'],
                weather_data['city']
            )
            forecast_data = WeatherService.get_forecast_data(city_searched)
    
    elif profile.saved_location_city:
        weather_data = WeatherService.get_weather_data(profile.saved_location_city)
        if weather_data and 'error' not in weather_data:
            forecast_data = WeatherService.get_forecast_data(profile.saved_location_city)
            suggestions = ActivityService.get_suggestions(
                weather_data['description'],
                weather_data['temperature']
            )
    
    is_favorite = False
    if weather_data and 'error' not in weather_data:
        is_favorite = FavoriteCity.objects.filter(
            user=request.user, city_name=weather_data['city']
        ).exists()
    
    context = {
        'weather_data': weather_data,
        'forecast_data': forecast_data,
        'suggestions': suggestions,
        'is_favorite': is_favorite,
        'has_weather_data': weather_data and 'error' not in weather_data,
        'has_saved_location': bool(profile.saved_location_city),
    }
    return render(request, 'weatherwise/home.html', context)

@login_required
def favorites_view(request):
    """User's favorite cities page"""
    from accounts.models import FavoriteCity
    
    favorites = FavoriteCity.objects.filter(user=request.user)
    favorite_weather = []
    latest_favorite = None
    latest_favorite_weather = None
    
    for fav in favorites:
        weather = WeatherService.get_weather_data(fav.city_name)
        if weather and 'error' not in weather:
            weather['fav_id'] = fav.id
            favorite_weather.append(weather)
    
    # Get the latest added favorite (first one by added_at descending)
    if favorites.exists():
        latest_favorite = favorites.first()  # Gets the most recent
        latest_favorite_weather = WeatherService.get_weather_data(latest_favorite.city_name)
        if latest_favorite_weather and 'error' in latest_favorite_weather:
            latest_favorite_weather = None
    
    context = {
        'favorites': favorite_weather,
        'latest_favorite': latest_favorite,
        'latest_favorite_weather': latest_favorite_weather,
    }
    return render(request, 'weatherwise/favorites.html', context)

@login_required
def profile_view(request):
    search_history = WeatherSearch.objects.filter(user=request.user)[:20]
    
    context = {
        'search_history': search_history,
    }
    return render(request, 'weatherwise/profile.html', context)

@login_required
def clear_search_history(request):
    if request.method == 'POST':
        count = WeatherSearch.objects.filter(user=request.user).count()
        WeatherSearch.objects.filter(user=request.user).delete()
        
        if count > 0:
            messages.success(request, f'✓ Successfully cleared {count} search history items!')
        else:
            messages.info(request, 'Your search history was already empty.')
        
        return redirect('weatherwise:profile')
    
    return redirect('weatherwise:profile')

@login_required
def save_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            city = data.get('city')
            
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.saved_location_city = city
            profile.save()
            
            return JsonResponse({'status': 'success', 'city': city})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error'}, status=400)

# ==================== AJAX ENDPOINTS ====================

@login_required
def toggle_favorite(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            city = data.get('city')
            country = data.get('country', '')
            
            favorite = FavoriteCity.objects.filter(user=request.user, city_name=city).first()
            
            if favorite:
                favorite.delete()
                return JsonResponse({'status': 'removed'})
            else:
                FavoriteCity.objects.create(
                    user=request.user,
                    city_name=city,
                    country=country
                )
                return JsonResponse({'status': 'added'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def check_favorite(request):
    city = request.GET.get('city')
    if not city:
        return JsonResponse({'is_favorite': False})
    
    is_favorite = FavoriteCity.objects.filter(
        user=request.user, city_name=city
    ).exists()
    
    return JsonResponse({'is_favorite': is_favorite})

@login_required
def save_theme(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            theme = data.get('theme')
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.theme_preference = theme
            profile.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def save_unit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            unit = data.get('unit')
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.preferred_unit = unit
            profile.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

# ==================== API VIEWS ====================

@api_view(['GET'])
def weather_by_coordinates(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    if not lat or not lon:
        return Response({'error': 'Coordinates required'}, status=400)
    
    weather = WeatherService.get_weather_by_coordinates(float(lat), float(lon))
    return Response(weather)

@api_view(['GET', 'POST'])
def weather_api(request):
    """API endpoint for weather data"""
    if request.method == 'GET':
        city = request.GET.get('city')
        if not city:
            return Response({'error': 'City required'}, status=400)
        
        weather = WeatherService.get_weather_data(city)
        return Response(weather)
    
    elif request.method == 'POST':
        print("=" * 50)
        print("POST request received to /api/weather/")
        print("Request body:", request.body)
        print("User authenticated:", request.user.is_authenticated)
        print("User:", request.user if request.user.is_authenticated else "Anonymous")
        
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            city = serializer.validated_data['city']
            print(f"City: {city}")
            
            weather_data = WeatherService.get_weather_data(city)
            print(f"Weather data: {weather_data}")
            
            if 'error' in weather_data:
                return Response({'status': 'error', 'message': weather_data['error']},
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Save to search history for the logged-in user
            if request.user.is_authenticated:
                try:
                    search = WeatherSearch.objects.create(
                        user=request.user,
                        city=weather_data['city'],
                        country=weather_data['country'],
                        temperature=weather_data['temperature'],
                        feels_like=weather_data['feels_like'],
                        description=weather_data['description'],
                        icon=weather_data['icon'],
                        humidity=weather_data['humidity'],
                        wind_speed=weather_data['wind_speed'],
                        pressure=weather_data['pressure']
                    )
                    print(f"Search saved with ID: {search.id}")
                except Exception as e:
                    print(f"Error saving search: {e}")
            else:
                print("User not authenticated - not saving to history")
            
            return Response({'status': 'success', 'data': weather_data})
        
        print(f"Serializer errors: {serializer.errors}")
        return Response({'status': 'error', 'errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

@login_required
def favorite_activity_api(request):
    """Save or update favorite activity for a city"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            city = data.get('city')
            country = data.get('country', '')
            activity_note = data.get('activity_note', '')
            
            favorite_activity, created = UserFavoriteActivity.objects.update_or_create(
                user=request.user,
                city_name=city,
                defaults={
                    'country': country,
                    'activity_note': activity_note
                }
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Favorite activity saved!',
                'created': created
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def get_favorite_activity_api(request):
    """Get favorite activity for a city"""
    city = request.GET.get('city')
    if not city:
        return JsonResponse({'status': 'error', 'message': 'City required'}, status=400)
    
    try:
        favorite_activity = UserFavoriteActivity.objects.get(
            user=request.user,
            city_name=city
        )
        return JsonResponse({
            'status': 'success',
            'activity_note': favorite_activity.activity_note,
            'city': favorite_activity.city_name,
            'country': favorite_activity.country
        })
    except UserFavoriteActivity.DoesNotExist:
        return JsonResponse({'status': 'success', 'activity_note': ''})

@login_required
def toggle_hearted_activity(request):
    """Save or remove hearted activity to database"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            city = data.get('city')
            country = data.get('country', '')
            activity = data.get('activity')
            detail = data.get('detail', '')
            icon = data.get('icon', '')
            
            # Check if already hearted
            hearted = HeartedActivity.objects.filter(
                user=request.user,
                city=city,
                activity=activity
            ).first()
            
            if hearted:
                hearted.delete()
                return JsonResponse({'status': 'removed'})
            else:
                HeartedActivity.objects.create(
                    user=request.user,
                    city=city,
                    country=country,
                    activity=activity,
                    detail=detail,
                    icon=icon
                )
                return JsonResponse({'status': 'added'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def get_hearted_activities(request):
    """Get all hearted activities for current user"""
    activities = HeartedActivity.objects.filter(user=request.user)
    data = []
    for act in activities:
        data.append({
            'city': act.city,
            'country': act.country,
            'activity': act.activity,
            'detail': act.detail,
            'icon': act.icon,
            'timestamp': act.created_at.timestamp()
        })
    return JsonResponse({'activities': data})