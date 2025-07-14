from flask import Blueprint, request, jsonify
from src.models import db, DefectCode
from src.utils.decorators import role_required

defect_code_bp = Blueprint('defect_code', __name__)

@defect_code_bp.route('/', methods=['GET'])
def get_defect_codes():
    defect_codes = DefectCode.query.filter_by(is_active=True).all()
    return jsonify([dc.to_dict() for dc in defect_codes]), 200

@defect_code_bp.route('/<int:defect_code_id>', methods=['GET'])
def get_defect_code(defect_code_id):
    defect_code = DefectCode.query.get_or_404(defect_code_id)
    return jsonify(defect_code.to_dict()), 200

@defect_code_bp.route('/', methods=['POST'])
@role_required('admin')
def create_defect_code():
    data = request.get_json()
    if not all(field in data for field in ['code', 'description']):
        return jsonify({'error': 'Code and description are required'}), 400
    
    existing = DefectCode.query.filter_by(code=data['code']).first()
    if existing:
        return jsonify({'error': 'Defect code already exists'}), 400
    
    defect_code = DefectCode(
        code=data['code'],
        description=data['description'],
        category=data.get('category')
    )
    db.session.add(defect_code)
    db.session.commit()
    return jsonify(defect_code.to_dict()), 201

@defect_code_bp.route('/<int:defect_code_id>', methods=['PUT'])
@role_required('admin')
def update_defect_code(defect_code_id):
    defect_code = DefectCode.query.get_or_404(defect_code_id)
    data = request.get_json()
    
    if 'code' in data and data['code'] != defect_code.code:
        existing = DefectCode.query.filter_by(code=data['code']).first()
        if existing:
            return jsonify({'error': 'Defect code already exists'}), 400
        defect_code.code = data['code']
    
    if 'description' in data:
        defect_code.description = data['description']
    
    if 'category' in data:
        defect_code.category = data['category']
    
    if 'is_active' in data:
        defect_code.is_active = data['is_active']
    
    db.session.commit()
    return jsonify(defect_code.to_dict()), 200

@defect_code_bp.route('/<int:defect_code_id>', methods=['DELETE'])
@role_required('admin')
def delete_defect_code(defect_code_id):
    defect_code = DefectCode.query.get_or_404(defect_code_id)
    defect_code.is_active = False
    db.session.commit()
    return jsonify({'message': 'Defect code deactivated successfully'}), 200