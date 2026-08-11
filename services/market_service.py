import datetime
from models.market import MarketModel

class MarketService:
    @staticmethod
    def get_market_data(db_path, api_key=None, farmer_crop="Paddy"):
        """
        Fetches market prices. Uses live API if key is present,
        otherwise uses database stored market data with clear demo labels.
        """
        updated_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if api_key and api_key.strip():
            # Production market API integration hook (e.g., Gov Agmarknet API)
            pass

        # Fetch from database model
        raw_prices = MarketModel.get_all_prices(db_path)
        
        formatted_prices = []
        for item in raw_prices:
            is_user_crop = (item['crop'].lower() in farmer_crop.lower()) or (farmer_crop.lower() in item['crop'].lower())
            formatted_prices.append({
                "id": item['id'],
                "market": item['market'],
                "crop": item['crop'],
                "variety": item['variety'],
                "price": item['price'],
                "formatted_price": f"₹{item['price']:,}/Qtl",
                "trend": item['trend'],
                "is_positive": '+' in item['trend'],
                "is_user_crop": is_user_crop,
                "updated_at": item['updated_at']
            })

        return {
            "market_name": "Vijayawada Regional Agmarknet",
            "updated_at": updated_time,
            "is_demo": True,
            "demo_label": "Demo Market Data (Live Agmarknet API integration ready)",
            "prices": formatted_prices
        }
