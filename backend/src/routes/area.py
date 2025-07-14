from flask import Blueprint, request, jsonify
from src.models import db, Area
from src.utils.decorators import role_required

area_bp = Blueprint('area', __name__)

@area_bp.route('/', methods=['GET'])
def get_areas():
    areas = Area.query.filter_by(is_active=True).all()
    return jsonify([area.to_dict() for area in areas]), 200

@area_bp.route('/<int:area_id>', methods=['GET'])
def get_area(area_id):
    area = Area.query.get_or_404(area_id)
    return jsonify(area.to_dict()), 200

@area_bp.route('/', methods=['POST'])
@role_required('admin')
def create_area():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    existing = Area.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({'error': 'Area name already exists'}), 400
    
    area = Area(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(area)
    db.session.commit()
    return jsonify(area.to_dict()), 201

@area_bp.route('/<int:area_id>', methods=['PUT'])
@role_required('admin')
def update_area(area_id):
    area = Area.query.get_or_404(area_id)
    data = request.get_json()
    
    if 'name' in data and data['name'] != area.name:
        existing = Area.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Area name already exists'}), 400
        area.name = data['name']
    
    if 'description' in data:
        area.description = data['description']
    
    if 'is_active' in data:
        area.is_active = data['is_active']
    
    db.session.commit()
    return jsonify(area.to_dict()), 200

@area_bp.route('/<int:area_id>', methods=['DELETE'])
@role_required('admin')
def delete_area(area_id):
    area = Area.query.get_or_404(area_id)
    area.is_active = False
    db.session.commit()
    return jsonify({'message': 'Area deactivated successfully'}), 200