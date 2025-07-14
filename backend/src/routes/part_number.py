from flask import Blueprint, request, jsonify
from src.models import db, PartNumber
from src.utils.decorators import role_required

part_number_bp = Blueprint('part_number', __name__)

@part_number_bp.route('/', methods=['GET'])
def get_part_numbers():
    customer_id = request.args.get('customer_id')
    query = PartNumber.query.filter_by(is_active=True)
    
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    
    part_numbers = query.all()
    return jsonify([pn.to_dict() for pn in part_numbers]), 200

@part_number_bp.route('/<int:part_number_id>', methods=['GET'])
def get_part_number(part_number_id):
    part_number = PartNumber.query.get_or_404(part_number_id)
    return jsonify(part_number.to_dict()), 200

@part_number_bp.route('/', methods=['POST'])
@role_required('admin')
def create_part_number():
    data = request.get_json()
    required_fields = ['part_number', 'customer_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check for existing part number for this customer
    existing = PartNumber.query.filter_by(
        part_number=data['part_number'],
        customer_id=data['customer_id']
    ).first()
    
    if existing:
        return jsonify({'error': 'Part number already exists for this customer'}), 400
    
    part_number = PartNumber(
        part_number=data['part_number'],
        customer_id=data['customer_id'],
        description=data.get('description'),
        oven_program=data.get('oven_program'),
        oven_steps=data.get('oven_steps'),
        oven_details=data.get('oven_details'),
        notes=data.get('notes')
    )
    db.session.add(part_number)
    db.session.commit()
    return jsonify(part_number.to_dict()), 201

@part_number_bp.route('/<int:part_number_id>', methods=['PUT'])
@role_required('admin')
def update_part_number(part_number_id):
    part_number = PartNumber.query.get_or_404(part_number_id)
    data = request.get_json()
    
    if 'part_number' in data and data['part_number'] != part_number.part_number:
        existing = PartNumber.query.filter_by(
            part_number=data['part_number'],
            customer_id=part_number.customer_id
        ).first()
        if existing:
            return jsonify({'error': 'Part number already exists for this customer'}), 400
        part_number.part_number = data['part_number']
    
    if 'description' in data:
        part_number.description = data['description']
    
    if 'oven_program' in data:
        part_number.oven_program = data['oven_program']
    
    if 'oven_steps' in data:
        part_number.oven_steps = data['oven_steps']
    
    if 'oven_details' in data:
        part_number.oven_details = data['oven_details']
    
    if 'notes' in data:
        part_number.notes = data['notes']
    
    if 'is_active' in data:
        part_number.is_active = data['is_active']
    
    db.session.commit()
    return jsonify(part_number.to_dict()), 200

@part_number_bp.route('/<int:part_number_id>', methods=['DELETE'])
@role_required('admin')
def delete_part_number(part_number_id):
    part_number = PartNumber.query.get_or_404(part_number_id)
    part_number.is_active = False
    db.session.commit()
    return jsonify({'message': 'Part number deactivated successfully'}), 200