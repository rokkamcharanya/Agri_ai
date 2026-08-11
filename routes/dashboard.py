from flask import Blueprint, render_template, session, redirect, url_for, current_app
from models.user import User
from models.farm import Farm
from models.crop_analysis import CropAnalysisModel
from services.weather_service import WeatherService
from services.risk_engine import RiskEngine
from services.market_service import MarketService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard_view'))
    return redirect(url_for('auth.login'))

@dashboard_bp.route('/dashboard')
def dashboard_view():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    db_path = current_app.config['DATABASE_PATH']
    api_key = current_app.config['WEATHER_API_KEY']
    market_key = current_app.config['MARKET_API_KEY']

    user = User.get_by_id(db_path, user_id)
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))

    farm = Farm.get_by_user_id(db_path, user_id)
    latest_analysis = CropAnalysisModel.get_latest_for_user(db_path, user_id)
    
    # Weather telemetry
    lat = farm['latitude'] if farm else current_app.config['DEFAULT_LAT']
    lon = farm['longitude'] if farm else current_app.config['DEFAULT_LON']
    loc_name = farm['location_name'] if farm else current_app.config['DEFAULT_LOCATION']
    
    weather = WeatherService.get_weather(api_key, lat, lon, loc_name)

    crop_name = farm['crop_name'] if farm else 'Paddy'
    health_score = latest_analysis['health_score'] if latest_analysis else 86
    health_status = latest_analysis['condition'] if latest_analysis else 'Healthy'

    # Upcoming farm risks
    risks = RiskEngine.calculate_crop_risks(crop_name, weather, health_score, loc_name)

    # Market prices
    market_data = MarketService.get_market_data(db_path, market_key, farmer_crop=crop_name)

    return render_template(
        'dashboard.html',
        user=user,
        farm=farm,
        latest_analysis=latest_analysis,
        weather=weather,
        risks=risks,
        market_data=market_data,
        crop_name=crop_name,
        health_score=health_score,
        health_status=health_status,
        location_name=loc_name
    )
