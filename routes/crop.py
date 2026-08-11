import os
import uuid
from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.utils import secure_filename
from models.farm import Farm
from models.crop_analysis import CropAnalysisModel
from services.crop_ai import CropAIService

crop_bp = Blueprint('crop', __name__)
crop_ai_service = CropAIService()

def allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return ext in current_app.config['ALLOWED_EXTENSIONS']

@crop_bp.route('/api/crop/analyze', methods=['POST'])
def analyze_crop():
    if 'user_id' not in session:
        return jsonify({"error": "Authentication required"}), 401

    if 'crop_image' not in request.files:
        return jsonify({"error": "No crop image file provided"}), 400

    file = request.files['crop_image']
    if file.filename == '':
        return jsonify({"error": "No selected image file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file format. Please upload PNG, JPG, JPEG, or WEBP images."}), 400

    user_id = session['user_id']
    db_path = current_app.config['DATABASE_PATH']
    farm = Farm.get_by_user_id(db_path, user_id)
    farm_id = farm['id'] if farm else 1
    crop_hint = farm['crop_name'] if farm else 'Paddy'

    # Save uploaded file securely
    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)

    relative_image_path = f"/static/uploads/{filename}"

    try:
        analysis = crop_ai_service.analyze_image(save_path, crop_hint=crop_hint)

        # Store analysis record in database
        analysis_id = CropAnalysisModel.save_analysis(
            db_path=db_path,
            user_id=user_id,
            farm_id=farm_id,
            image_path=relative_image_path,
            crop_name=analysis['crop_name'],
            condition=analysis['condition'],
            health_score=analysis['health_score'],
            disease=analysis['disease'],
            disease_risk=analysis['disease_risk'],
            confidence=analysis['confidence'],
            recommendation=analysis['recommendation']
        )

        analysis['id'] = analysis_id
        analysis['image_path'] = relative_image_path
        return jsonify({"success": True, "analysis": analysis})

    except Exception as e:
        return jsonify({"error": f"Failed to analyze image: {str(e)}"}), 500

@crop_bp.route('/api/crop/history', methods=['GET'])
def crop_history():
    if 'user_id' not in session:
        return jsonify({"error": "Authentication required"}), 401

    user_id = session['user_id']
    db_path = current_app.config['DATABASE_PATH']
    records = CropAnalysisModel.get_history_for_user(db_path, user_id, limit=7)

    result = []
    for r in records:
        result.append({
            "id": r['id'],
            "crop_name": r['crop_name'],
            "condition": r['condition'],
            "health_score": r['health_score'],
            "disease": r['disease'],
            "disease_risk": r['disease_risk'],
            "created_at": r['created_at']
        })

    return jsonify({"history": result})
