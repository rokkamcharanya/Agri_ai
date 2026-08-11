import sqlite3
import os

def get_db_connection(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        mobile TEXT UNIQUE,
        email TEXT UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 2. Farms Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS farms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        crop_name TEXT DEFAULT 'Paddy',
        variety TEXT DEFAULT 'BPT 5204',
        latitude REAL DEFAULT 16.5062,
        longitude REAL DEFAULT 80.6480,
        location_name TEXT DEFAULT 'Vijayawada, Andhra Pradesh',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # 3. Crop Analysis History Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS crop_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        farm_id INTEGER NOT NULL,
        image_path TEXT,
        crop_name TEXT NOT NULL,
        condition TEXT NOT NULL,
        health_score INTEGER NOT NULL,
        disease TEXT NOT NULL,
        disease_risk TEXT NOT NULL,
        confidence INTEGER NOT NULL,
        recommendation TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (farm_id) REFERENCES farms (id)
    )
    ''')

    # 4. Weather History Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farm_id INTEGER NOT NULL,
        temperature REAL NOT NULL,
        humidity INTEGER NOT NULL,
        rainfall REAL NOT NULL,
        rain_probability INTEGER NOT NULL,
        weather_condition TEXT NOT NULL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (farm_id) REFERENCES farms (id)
    )
    ''')

    # 5. Market Prices Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS market_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        market TEXT NOT NULL,
        crop TEXT NOT NULL,
        variety TEXT NOT NULL,
        price INTEGER NOT NULL,
        trend TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_demo BOOLEAN DEFAULT 1
    )
    ''')

    conn.commit()

    # Seed initial demo market data if table is empty
    cursor.execute('SELECT COUNT(*) FROM market_prices')
    if cursor.fetchone()[0] == 0:
        demo_prices = [
            ('Vijayawada Market', 'Paddy', 'BPT 5204', 2350, '+3.2%', 1),
            ('Vijayawada Market', 'Maize', 'Yellow Hybrid', 2100, '+1.8%', 1),
            ('Guntur Market', 'Chilli', 'Teja / Guntur', 8500, '-2.1%', 1),
            ('Eluru Market', 'Groundnut', 'Bold Grade-1', 6200, '+2.5%', 1),
            ('Guntur Market', 'Cotton', 'H4 / Long Staple', 7100, '+0.5%', 1)
        ]
        cursor.executemany('''
            INSERT INTO market_prices (market, crop, variety, price, trend, is_demo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', demo_prices)

    # Seed initial historical crop analysis data if empty for demo graph
    cursor.execute('SELECT COUNT(*) FROM crop_analysis')
    if cursor.fetchone()[0] == 0:
        import datetime
        today = datetime.date.today()
        # Seed 7 days of historical crop health records for initial demo user (user_id = 1, farm_id = 1)
        demo_history = [
            (1, 1, '/static/uploads/sample1.jpg', 'Paddy', 'Healthy', 92, 'None Detected', 'Low', 96, 'Maintain regular irrigation and monitoring.', (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d %H:%M:%S')),
            (1, 1, '/static/uploads/sample2.jpg', 'Paddy', 'Healthy', 90, 'None Detected', 'Low', 95, 'Ensure optimal NPK balance.', (today - datetime.timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S')),
            (1, 1, '/static/uploads/sample3.jpg', 'Paddy', 'Good', 88, 'Minor Spot Risk', 'Low', 92, 'Inspect lower leaves weekly.', (today - datetime.timedelta(days=4)).strftime('%Y-%m-%d %H:%M:%S')),
            (1, 1, '/static/uploads/sample4.jpg', 'Paddy', 'Good', 87, 'Leaf Blight Suspected', 'Medium', 89, 'Apply recommended neem oil spray.', (today - datetime.timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')),
            (1, 1, '/static/uploads/sample5.jpg', 'Paddy', 'Fair', 84, 'Fungal Moisture Stress', 'Medium', 88, 'Ensure proper field drainage before rains.', (today - datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')),
            (1, 1, '/static/uploads/sample6.jpg', 'Paddy', 'Good', 85, 'Early Leaf Blast Risk', 'Medium', 91, 'Monitor humidity and clear weed bunds.', (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')),
            (1, 1, '/static/uploads/sample7.jpg', 'Paddy', 'Healthy', 86, 'Mild Nutrient Strain', 'Medium', 94, 'Continue regular monitoring and maintain proper irrigation.', today.strftime('%Y-%m-%d %H:%M:%S'))
        ]
        cursor.executemany('''
            INSERT INTO crop_analysis (user_id, farm_id, image_path, crop_name, condition, health_score, disease, disease_risk, confidence, recommendation, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', demo_history)

    conn.commit()
    conn.close()
