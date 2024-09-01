from flask import Blueprint, request, jsonify
from .services.verification_service import verify_employee
import os
from werkzeug.utils import secure_filename
import tempfile

main_bp = Blueprint('main', __name__)

@main_bp.route('/verify', methods=['POST'])
def verify():
    if 'file' not in request.files or 'employee_id' not in request.form:
        return jsonify({"error": "No file or employee_id provided"}), 400
    
    file = request.files['file']
    employee_id = request.form['employee_id']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        file_path = temp_file.name
        file.save(file_path)
    
    try:
        result = verify_employee(file_path, employee_id)
        if result:
            return jsonify({"status": "Verified"})
        else:
            return jsonify({"status": "Verification failed"}), 400
    finally:
        os.remove(file_path)
