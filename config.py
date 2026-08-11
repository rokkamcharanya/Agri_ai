import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'agri-ai-super-secret-key-2026-hackathon'
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or os.path.join(BASE_DIR, 'database', 'database.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    # Weather API config
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or ''
    
    # Live market API config
    MARKET_API_KEY = os.environ.get('MARKET_API_KEY') or ''
    
    # Default location if geolocation is denied
    DEFAULT_LOCATION = "Vijayawada, Andhra Pradesh"
    DEFAULT_LAT = 16.5062
    DEFAULT_LON = 80.6480
