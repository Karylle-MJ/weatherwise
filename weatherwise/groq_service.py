import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class GroqService:
    """Service to generate AI-powered activity suggestions using GroqCloud - NO FALLBACKS"""
    
    @staticmethod
    def get_activity_suggestions(weather_description, temperature, city_name):
        """Generate dynamic activity suggestions using Groq's fast inference - AI ONLY"""
        
        # Check if API key is configured
        if not hasattr(settings, 'GROQ_API_KEY') or not settings.GROQ_API_KEY:
            error_msg = "Groq API key not configured. Please add GROQ_API_KEY to settings.py"
            logger.error(error_msg)
            return [{"icon": "❌", "activity": "API Key Missing", "detail": error_msg}]
        
        try:
            # Import Groq library
            from groq import Groq
            
            # Initialize the Groq client
            client = Groq(api_key=settings.GROQ_API_KEY)
            
            # Create a prompt for the AI
            prompt = f"""You are a helpful weather activity assistant. Based on the current weather in {city_name}, suggest 4 activities.

Weather conditions: {weather_description}
Temperature: {temperature}°C

Respond with ONLY valid JSON in this exact format, no other text, no markdown:
[
    {{"icon": "emoji", "activity": "activity name", "detail": "brief description (5-10 words)"}}
]

Use appropriate emojis. Be practical and safety-conscious for the weather conditions and its location."""
            
            # Call Groq API
            completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that suggests activities based on weather. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            # Get the response
            ai_response = completion.choices[0].message.content
            print(f"🤖 Groq AI Response: {ai_response[:200]}...")
            
            # Parse JSON response
            suggestions = json.loads(ai_response)
            
            # Handle different response formats
            if isinstance(suggestions, dict):
                if 'activities' in suggestions:
                    suggestions = suggestions['activities']
                elif 'suggestions' in suggestions:
                    suggestions = suggestions['suggestions']
            
            if isinstance(suggestions, list) and len(suggestions) > 0:
                return suggestions[:4]
            else:
                return [{"icon": "⚠️", "activity": "Invalid Response", "detail": "AI returned unexpected format"}]
                
        except ImportError:
            error_msg = "groq library not installed. Run: pip install groq"
            logger.error(error_msg)
            return [{"icon": "❌", "activity": "Library Missing", "detail": error_msg}]
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse AI response: {str(e)}"
            logger.error(error_msg)
            return [{"icon": "⚠️", "activity": "Parsing Error", "detail": "AI response was not valid JSON"}]
        except Exception as e:
            error_msg = f"Groq API error: {str(e)}"
            logger.error(error_msg)
            return [{"icon": "❌", "activity": "API Error", "detail": "Unable to fetch AI suggestions. Please try again."}]