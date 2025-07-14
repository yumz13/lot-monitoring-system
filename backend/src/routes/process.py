from flask import Blueprint, request, jsonify
from src.models import db, Process
from src.utils.decorators import role_required

process_bp = Blueprint('process', __name__)

@process_bp.route('/', methods=['GET'])
def get_processes():
    processes = Process.query.filter_by(is_active=True).order_by(Process.order_sequence).all()
    return jsonify([process.to_dict() for process in processes]), 200

@process_bp.route('/<int:process_id>', methods=['GET'])
def get_process(process_id):
    process = Process.query.get_or_404(process_id)
    return jsonify(process.to_dict()), 200

@process_bp.route('/', methods=['POST'])
@role_required('admin')
def create_process():
    data = request.get_json()
    required_fields = ['name', 'order_sequence']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check for existing process name or order sequence
    existing_name = Process.query.filter_by(name=data['name']).first()
    existing_order = Process.query.filter_by(order_sequence=data['order_sequence']).first()
    
    if existing_name:
        return jsonify({'error': 'Process name already exists'}), 400
    if existing_order:
        return jsonify({'error': 'Order sequence already in use'}), 400
    
    process = Process(
        name=data['name'],
        order_sequence=data['order_sequence'],
        description=data.get('description')
    )
    db.session.add(process)
    db.session.commit()
    return jsonify(process.to_dict()), 201

@process_bp.route('/<int:process_id>', methods=['PUT'])
@role_required('admin')
def update_process(process_id):
    process = Process.query.get_or_404(process_id)
    data = request.get_json()
    
    if 'name' in data and data['name'] != process.name:
        existing = Process.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Process name already exists'}), 400
        process.name = data['name']
    
    if 'order_sequence' in data and data['order_sequence'] != process.order_sequence:
        existing = Process.query.filter_by(order_sequence=data['order_sequence']).first()
        if existing:
            return jsonify({'error': 'Order sequence already in use'}), 400
        process.order_sequence = data['order_sequence']
    
    if 'description' in data:
        process.description = data['description']
    
    if 'is_active' in data:
        process.is_active = data['is_active']
    
    db.session.commit()
    return jsonify(process.to_dict()), 200

@process_bp.route('/<int:process_id>', methods=['DELETE'])
@role_required('admin')
def delete_process(process_id):
    process = Process.query.get_or_404(process_id)
    process.is_active = False
    db.session.commit()
    return jsonify({'message': 'Process deactivated successfully'}), 200