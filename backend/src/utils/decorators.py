from functools import wraps
from flask import request, jsonify
import jwt
from src.app import current_app

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'error': 'Authorization token missing'}), 401
            
            try:
                token = token.split()[1]  # Remove 'Bearer ' prefix
                payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
                
                if payload.get('role') != required_role:
                    return jsonify({'error': 'Insufficient permissions'}), 403
                
                return f(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401
        
        return decorated_function
    return decorator

def validate_json(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400
            
            for field, field_type in schema.items():
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
                if not isinstance(data[field], field_type):
                    return jsonify({'error': f'Invalid type for field: {field}'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator