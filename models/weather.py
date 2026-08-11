from database.db import get_db_connection

class WeatherModel:
    @staticmethod
    def save_weather(db_path, farm_id, temperature, humidity, rainfall, rain_probability, weather_condition):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO weather_history (farm_id, temperature, humidity, rainfall, rain_probability, weather_condition)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (farm_id, temperature, humidity, rainfall, rain_probability, weather_condition))
        weather_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return weather_id

    @staticmethod
    def get_latest_for_farm(db_path, farm_id):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM weather_history
            WHERE farm_id = ?
            ORDER BY recorded_at DESC LIMIT 1
        ''', (farm_id,))
        record = cursor.fetchone()
        conn.close()
        return record
