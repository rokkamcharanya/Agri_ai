from database.db import get_db_connection

class Farm:
    @staticmethod
    def get_by_user_id(db_path, user_id):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM farms WHERE user_id = ? ORDER BY id DESC LIMIT 1', (user_id,))
        farm = cursor.fetchone()
        conn.close()
        return farm

    @staticmethod
    def update_farm_details(db_path, user_id, crop_name=None, variety=None, latitude=None, longitude=None, location_name=None):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        farm = Farm.get_by_user_id(db_path, user_id)
        
        if not farm:
            cursor.execute('''
                INSERT INTO farms (user_id, crop_name, variety, latitude, longitude, location_name)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                crop_name or 'Paddy',
                variety or 'BPT 5204',
                latitude or 16.5062,
                longitude or 80.6480,
                location_name or 'Vijayawada, Andhra Pradesh'
            ))
        else:
            updated_crop = crop_name if crop_name is not None else farm['crop_name']
            updated_variety = variety if variety is not None else farm['variety']
            updated_lat = latitude if latitude is not None else farm['latitude']
            updated_lon = longitude if longitude is not None else farm['longitude']
            updated_loc = location_name if location_name is not None else farm['location_name']
            
            cursor.execute('''
                UPDATE farms
                SET crop_name = ?, variety = ?, latitude = ?, longitude = ?, location_name = ?
                WHERE id = ?
            ''', (updated_crop, updated_variety, updated_lat, updated_lon, updated_loc, farm['id']))
            
        conn.commit()
        conn.close()
