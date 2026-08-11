import os
from flask import Flask, render_template
from config import Config
from database.db import init_db

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    # Initialize SQLite Database & Tables
    init_db(app.config['DATABASE_PATH'])

    # Ensure uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.crop import crop_bp
    from routes.weather import weather_bp
    from routes.market import market_bp
    from routes.voice import voice_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(crop_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(market_bp)
    app.register_blueprint(voice_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('login.html', error="Page not found. Redirected to login."), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('login.html', error="Internal server error occurred. Please try again."), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
