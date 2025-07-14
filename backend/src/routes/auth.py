from flask import Blueprint, request, jsonify
from src.services.auth_service import AuthService
from src.utils.decorators import validate_json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@validate_json({'card_number': str, 'area_id': int, 'process_id': int})
def login():
    data = request.get_json()
    result, error = AuthService.login_employee(
        data['card_number'],
        data['area_id'],
        data['process_id']
    )
    if error:
        return jsonify({'error': error}), 401
    return jsonify(result), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Authorization token missing'}), 401
    
    payload, error = AuthService.validate_token(token.split()[1])
    if error:
        return jsonify({'error': error}), 401
    
    success, error = AuthService.logout_employee(payload['session_token'])
    if error:
        return jsonify({'error': error}), 400
    return jsonify({'message': 'Logged out successfully'}), 200