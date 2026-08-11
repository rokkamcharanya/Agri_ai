from database.db import get_db_connection

class MarketModel:
    @staticmethod
    def get_all_prices(db_path):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM market_prices ORDER BY id ASC')
        prices = cursor.fetchall()
        conn.close()
        return [dict(p) for p in prices]

    @staticmethod
    def get_prices_for_crop(db_path, crop_name):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM market_prices WHERE crop LIKE ? ORDER BY id ASC', (f'%{crop_name}%',))
        prices = cursor.fetchall()
        conn.close()
        return [dict(p) for p in prices]
