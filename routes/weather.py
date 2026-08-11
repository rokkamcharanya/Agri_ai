from flask import Blueprint, request, jsonify, session, current_app
from models.farm import Farm
from models.weather import WeatherModel
from services.weather_service import WeatherService

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/api/weather', methods=['GET'])
def get_weather_data():
    user_id = session.get('user_id')
    db_path = current_app.config['DATABASE_PATH']
    api_key = current_app.config['WEATHER_API_KEY']

    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    loc_name = request.args.get('location', type=str)

    if user_id and (lat is None or lon is None):
        farm = Farm.get_by_user_id(db_path, user_id)
        if farm:
            lat = lat or farm['latitude']
            lon = lon or farm['longitude']
            loc_name = loc_name or farm['location_name']

    lat = lat or current_app.config['DEFAULT_LAT']
    lon = lon or current_app.config['DEFAULT_LON']
    loc_name = loc_name or current_app.config['DEFAULT_LOCATION']

    weather = WeatherService.get_weather(api_key, lat, lon, loc_name)

    if user_id:
        farm = Farm.get_by_user_id(db_path, user_id)
        if farm:
            WeatherModel.save_weather(
                db_path=db_path,
                farm_id=farm['id'],
                temperature=weather['temperature'],
                humidity=weather['humidity'],
                rainfall=weather['rainfall'],
                rain_probability=weather['rain_probability'],
                weather_condition=weather['condition']
            )

    return jsonify(weather)

@weather_bp.route('/api/location', methods=['POST'])
def update_location():
    if 'user_id' not in session:
        return jsonify({"error": "Authentication required"}), 401

    data = request.get_json() or {}
    lat = data.get('latitude')
    lon = data.get('longitude')
    loc_name = data.get('location_name', 'Vijayawada, Andhra Pradesh')
    crop_name = data.get('crop_name')

    user_id = session['user_id']
    db_path = current_app.config['DATABASE_PATH']

    Farm.update_farm_details(
        db_path=db_path,
        user_id=user_id,
        crop_name=crop_name,
        latitude=lat,
        longitude=lon,
        location_name=loc_name
    )

    return jsonify({"success": True, "location_name": loc_name, "latitude": lat, "longitude": lon})
