class ActivityService:
    
    @staticmethod
    def get_suggestions(weather_description, temperature):
        desc = weather_description.lower()
        suggestions = []
        
        if 'clear' in desc or 'sunny' in desc:
            suggestions = [
                {"icon": "🥾", "activity": "Go for a hike", "detail": "Perfect day for outdoor adventure"},
                {"icon": "🧺", "activity": "Have a picnic", "detail": "Enjoy the sunshine outdoors"},
                {"icon": "🏖️", "activity": "Visit the beach", "detail": "Great for swimming"},
                {"icon": "⚽", "activity": "Play outdoor sports", "detail": "Ideal conditions for sports"}
            ]
        elif 'cloud' in desc:
            suggestions = [
                {"icon": "🚶", "activity": "Go for a walk", "detail": "Comfortable temperature for a stroll"},
                {"icon": "🏛️", "activity": "Visit a museum", "detail": "Explore art and history"},
                {"icon": "🛍️", "activity": "Go shopping", "detail": "Perfect day for mall exploration"},
                {"icon": "🎬", "activity": "Watch a movie", "detail": "Catch the latest films"}
            ]
        elif 'rain' in desc or 'drizzle' in desc:
            suggestions = [
                {"icon": "📚", "activity": "Read a book", "detail": "Cozy up with a good book"},
                {"icon": "☕", "activity": "Visit a café", "detail": "Warm up with a hot beverage"},
                {"icon": "🎮", "activity": "Play board games", "detail": "Fun indoor activity"},
                {"icon": "🏋️", "activity": "Indoor gym workout", "detail": "Stay fit despite the rain"}
            ]
        elif 'snow' in desc:
            suggestions = [
                {"icon": "⛄", "activity": "Build a snowman", "detail": "Enjoy the winter wonderland"},
                {"icon": "☕", "activity": "Hot chocolate time", "detail": "Warm up with a cozy drink"},
                {"icon": "⛸️", "activity": "Ice skating", "detail": "Fun winter activity"},
                {"icon": "📸", "activity": "Winter photography", "detail": "Capture beautiful snowy scenes"}
            ]
        else:
            suggestions = [
                {"icon": "🚶", "activity": "Take a walk", "detail": "Enjoy the fresh air"},
                {"icon": "🏠", "activity": "Relax at home", "detail": "Perfect time to unwind"},
                {"icon": "📖", "activity": "Learn something new", "detail": "Read or watch tutorials"}
            ]
        
        if temperature > 30:
            suggestions.append({"icon": "💧", "activity": "Stay hydrated", "detail": "Drink plenty of water"})
        elif temperature < 10:
            suggestions.append({"icon": "🧣", "activity": "Bundle up", "detail": "Wear warm clothes"})
        
        return suggestions[:4]