from flask import Blueprint, request, jsonify
from src.models import db, Customer
from src.utils.decorators import role_required

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/', methods=['GET'])
def get_customers():
    customers = Customer.query.filter_by(is_active=True).all()
    return jsonify([customer.to_dict() for customer in customers]), 200

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.to_dict()), 200

@customer_bp.route('/', methods=['POST'])
@role_required('admin')
def create_customer():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    existing = Customer.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({'error': 'Customer name already exists'}), 400
    
    customer = Customer(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201

@customer_bp.route('/<int:customer_id>', methods=['PUT'])
@role_required('admin')
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    
    if 'name' in data and data['name'] != customer.name:
        existing = Customer.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Customer name already exists'}), 400
        customer.name = data['name']
    
    if 'description' in data:
        customer.description = data['description']
    
    if 'is_active' in data:
        customer.is_active = data['is_active']
    
    db.session.commit()
    return jsonify(customer.to_dict()), 200

@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
@role_required('admin')
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer.is_active = False
    db.session.commit()
    return jsonify({'message': 'Customer deactivated successfully'}), 200