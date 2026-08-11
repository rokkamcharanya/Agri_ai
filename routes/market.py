from flask import Blueprint, jsonify, session, current_app
from models.farm import Farm
from services.market_service import MarketService

market_bp = Blueprint('market', __name__)

@market_bp.route('/api/market-prices', methods=['GET'])
def get_market_prices():
    db_path = current_app.config['DATABASE_PATH']
    market_key = current_app.config['MARKET_API_KEY']
    
    farmer_crop = "Paddy"
    if 'user_id' in session:
        user_id = session['user_id']
        farm = Farm.get_by_user_id(db_path, user_id)
        if farm:
            farmer_crop = farm['crop_name']

    market_data = MarketService.get_market_data(db_path, market_key, farmer_crop=farmer_crop)
    return jsonify(market_data)
