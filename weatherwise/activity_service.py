from .groq_service import GroqService

class ActivityService:
    
    @staticmethod
    def get_suggestions(weather_description, temperature, city_name=""):
        """
        Get activity suggestions using GroqCloud AI with fallback
        """
        return GroqService.get_activity_suggestions(
            weather_description, 
            temperature,
            city_name
        )