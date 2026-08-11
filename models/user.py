from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db_connection

class User:
    @staticmethod
    def create(db_path, name, mobile, email, password):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        password_hash = generate_password_hash(password)
        try:
            cursor.execute('''
                INSERT INTO users (name, mobile, email, password_hash)
                VALUES (?, ?, ?, ?)
            ''', (name, mobile or None, email or None, password_hash))
            user_id = cursor.lastrowid
            
            # Create a default farm entry for this user
            cursor.execute('''
                INSERT INTO farms (user_id, crop_name, variety, location_name)
                VALUES (?, 'Paddy', 'BPT 5204', 'Vijayawada, Andhra Pradesh')
            ''', (user_id,))
            
            conn.commit()
            return user_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_by_identifier(db_path, identifier):
        """Identifier can be email or mobile number."""
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users WHERE email = ? OR mobile = ?
        ''', (identifier, identifier))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def get_by_id(db_path, user_id):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def verify_password(user_row, password):
        if not user_row:
            return False
        return check_password_hash(user_row['password_hash'], password)

    @staticmethod
    def ensure_demo_user(db_path):
        """Creates demo farmer user if not exists."""
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE mobile = '9999999999' OR email = 'demo@agriai.org'")
        user = cursor.fetchone()
        if not user:
            password_hash = generate_password_hash('demo1234')
            cursor.execute('''
                INSERT INTO users (name, mobile, email, password_hash)
                VALUES ('Farmer Ramesh', '9999999999', 'demo@agriai.org', ?)
            ''', (password_hash,))
            user_id = cursor.lastrowid
            cursor.execute('''
                INSERT INTO farms (user_id, crop_name, variety, latitude, longitude, location_name)
                VALUES (?, 'Paddy', 'BPT 5204', 16.5062, 80.6480, 'Vijayawada, Andhra Pradesh')
            ''', (user_id,))
            conn.commit()
            conn.close()
            return user_id
        conn.close()
        return user['id']
