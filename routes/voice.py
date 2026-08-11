from flask import Blueprint, request, jsonify, session, current_app
from models.farm import Farm
from models.crop_analysis import CropAnalysisModel
from services.weather_service import WeatherService
from services.risk_engine import RiskEngine
from services.voice_service import VoiceAgronomistService

voice_bp = Blueprint('voice', __name__)

def _get_current_farm_context():
    user_id = session.get('user_id')
    db_path = current_app.config['DATABASE_PATH']
    api_key = current_app.config['WEATHER_API_KEY']

    farm = Farm.get_by_user_id(db_path, user_id) if user_id else None
    latest_analysis = CropAnalysisModel.get_latest_for_user(db_path, user_id) if user_id else None

    lat = farm['latitude'] if farm else current_app.config['DEFAULT_LAT']
    lon = farm['longitude'] if farm else current_app.config['DEFAULT_LON']
    loc_name = farm['location_name'] if farm else current_app.config['DEFAULT_LOCATION']

    weather = WeatherService.get_weather(api_key, lat, lon, loc_name)

    crop_name = farm['crop_name'] if farm else 'Paddy'
    health_score = latest_analysis['health_score'] if latest_analysis else 86
    condition = latest_analysis['condition'] if latest_analysis else 'Healthy'
    disease = latest_analysis['disease'] if latest_analysis else 'No Significant Disease Detected'
    disease_risk = latest_analysis['disease_risk'] if latest_analysis else 'Low'

    return {
        "crop_name": crop_name,
        "health_score": health_score,
        "condition": condition,
        "disease": disease,
        "disease_risk": disease_risk,
        "temperature": weather['temperature'],
        "rain_probability": weather['rain_probability'],
        "location": loc_name,
        "weather": weather
    }

@voice_bp.route('/api/voice/query', methods=['POST'])
def query_ai_agronomist():
    data = request.get_json() or {}
    query = data.get('query', '')
    lang = data.get('lang', 'en')

    if not query.strip():
        return jsonify({"error": "Query text cannot be empty"}), 400

    ctx = _get_current_farm_context()
    response = VoiceAgronomistService.answer_query(query, lang=lang, context=ctx)
    return jsonify(response)

@voice_bp.route('/api/risks', methods=['GET'])
def get_upcoming_risks():
    ctx = _get_current_farm_context()
    risks = RiskEngine.calculate_crop_risks(
        crop=ctx['crop_name'],
        weather=ctx['weather'],
        crop_health=ctx['health_score'],
        location=ctx['location']
    )
    return jsonify({"risks": risks})

@voice_bp.route('/api/voice/report', methods=['GET'])
def get_voice_report():
    lang = request.args.get('lang', 'en')
    ctx = _get_current_farm_context()
    report_text = VoiceAgronomistService.generate_full_crop_report(lang=lang, context=ctx)
    return jsonify({"report_text": report_text, "language": lang})
