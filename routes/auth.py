from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from models.user import User
from models.farm import Farm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard_view'))

    error = None
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '').strip()

        if not identifier or not password:
            error = "Please enter your mobile number or email and password."
        else:
            db_path = current_app.config['DATABASE_PATH']
            user = User.get_by_identifier(db_path, identifier)
            if user and User.verify_password(user, password):
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                return redirect(url_for('dashboard.dashboard_view'))
            else:
                error = "Invalid credentials. Please check your mobile/email and password."

    return render_template('login.html', error=error)

@auth_bp.route('/demo-login', methods=['POST', 'GET'])
def demo_login():
    db_path = current_app.config['DATABASE_PATH']
    user_id = User.ensure_demo_user(db_path)
    user = User.get_by_id(db_path, user_id)
    session['user_id'] = user['id']
    session['user_name'] = user['name']
    return redirect(url_for('dashboard.dashboard_view'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard_view'))

    error = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        mobile = request.form.get('mobile', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        crop_name = request.form.get('crop_name', 'Paddy').strip()

        if not name or not password or (not mobile and not email):
            error = "Please provide your name, password, and at least a mobile number or email."
        else:
            db_path = current_app.config['DATABASE_PATH']
            try:
                user_id = User.create(db_path, name, mobile, email, password)
                if crop_name:
                    Farm.update_farm_details(db_path, user_id, crop_name=crop_name)
                session['user_id'] = user_id
                session['user_name'] = name
                return redirect(url_for('dashboard.dashboard_view'))
            except Exception as e:
                error = f"Registration failed: Mobile or Email already exists."

    return render_template('register.html', error=error)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
