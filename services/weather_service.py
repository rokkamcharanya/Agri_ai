import requests

class WeatherService:
    @staticmethod
    def get_weather(api_key, lat=16.5062, lon=80.6480, location_name="Vijayawada, Andhra Pradesh"):
        """
        Fetches weather data from OpenWeatherMap API if key is available.
        Otherwise provides realistic, clearly-labeled demo weather data.
        """
        if api_key and api_key.strip():
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
                res = requests.get(url, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    temp = round(data['main']['temp'], 1)
                    humidity = data['main']['humidity']
                    wind_speed = round(data['wind']['speed'] * 3.6, 1) # convert to km/h
                    condition = data['weather'][0]['main']
                    
                    # Estimate rain probability based on humidity & clouds
                    clouds = data.get('clouds', {}).get('all', 50)
                    rain_prob = min(95, max(10, int((humidity * 0.6) + (clouds * 0.4))))
                    rainfall = data.get('rain', {}).get('1h', 0.0)
                    
                    return {
                        "location": data.get('name', location_name),
                        "latitude": lat,
                        "longitude": lon,
                        "temperature": temp,
                        "humidity": humidity,
                        "rainfall": rainfall,
                        "rain_probability": rain_prob,
                        "wind_speed": wind_speed,
                        "condition": condition,
                        "is_live": True,
                        "alert": "Heavy rainfall expected" if rain_prob > 70 else "Normal weather conditions"
                    }
            except Exception:
                pass # Fallback to structured demo data if network error or invalid API key

        # Fallback / Demo weather response (clearly marked)
        return {
            "location": location_name or "Vijayawada, Andhra Pradesh",
            "latitude": lat or 16.5062,
            "longitude": lon or 80.6480,
            "temperature": 32.0,
            "humidity": 72,
            "rainfall": 12.5,
            "rain_probability": 60,
            "wind_speed": 14.2,
            "condition": "Humid / Rain Expected",
            "is_live": False,
            "demo_label": "Demo Weather Data (Configure WEATHER_API_KEY for live feed)",
            "alert": "Heavy rainfall risk tomorrow. Check field drainage."
        }
