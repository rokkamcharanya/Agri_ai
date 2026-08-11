from database.db import get_db_connection

class CropAnalysisModel:
    @staticmethod
    def save_analysis(db_path, user_id, farm_id, image_path, crop_name, condition, health_score, disease, disease_risk, confidence, recommendation):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO crop_analysis (user_id, farm_id, image_path, crop_name, condition, health_score, disease, disease_risk, confidence, recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, farm_id, image_path, crop_name, condition, health_score, disease, disease_risk, confidence, recommendation))
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return analysis_id

    @staticmethod
    def get_latest_for_user(db_path, user_id):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM crop_analysis
            WHERE user_id = ?
            ORDER BY created_at DESC LIMIT 1
        ''', (user_id,))
        analysis = cursor.fetchone()
        conn.close()
        return analysis

    @staticmethod
    def get_history_for_user(db_path, user_id, limit=7):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM crop_analysis
            WHERE user_id = ?
            ORDER BY created_at ASC
            LIMIT ?
        ''', (user_id, limit))
        records = cursor.fetchall()
        conn.close()
        return records
