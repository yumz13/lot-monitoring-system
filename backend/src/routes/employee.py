from flask import Blueprint, request, jsonify
from src.models import db, Employee
from src.utils.decorators import role_required

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/', methods=['GET'])
@role_required('admin')
def get_employees():
    employees = Employee.query.filter_by(is_active=True).all()
    return jsonify([employee.to_dict() for employee in employees]), 200

@employee_bp.route('/<int:employee_id>', methods=['GET'])
@role_required('admin')
def get_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return jsonify(employee.to_dict()), 200

@employee_bp.route('/', methods=['POST'])
@role_required('admin')
def create_employee():
    data = request.get_json()
    required_fields = ['name', 'employee_id', 'card_number']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check for existing employee ID or card number
    existing_id = Employee.query.filter_by(employee_id=data['employee_id']).first()
    existing_card = Employee.query.filter_by(card_number=data['card_number']).first()
    
    if existing_id:
        return jsonify({'error': 'Employee ID already exists'}), 400
    if existing_card:
        return jsonify({'error': 'Card number already in use'}), 400
    
    employee = Employee(
        name=data['name'],
        employee_id=data['employee_id'],
        card_number=data['card_number'],
        department=data.get('department'),
        section=data.get('section'),
        role=data.get('role', 'operator')
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify(employee.to_dict()), 201

@employee_bp.route('/<int:employee_id>', methods=['PUT'])
@role_required('admin')
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    data = request.get_json()
    
    if 'employee_id' in data and data['employee_id'] != employee.employee_id:
        existing = Employee.query.filter_by(employee_id=data['employee_id']).first()
        if existing:
            return jsonify({'error': 'Employee ID already exists'}), 400
        employee.employee_id = data['employee_id']
    
    if 'card_number' in data and data['card_number'] != employee.card_number:
        existing = Employee.query.filter_by(card_number=data['card_number']).first()
        if existing:
            return jsonify({'error': 'Card number already in use'}), 400
        employee.card_number = data['card_number']
    
    if 'name' in data:
        employee.name = data['name']
    
    if 'department' in data:
        employee.department = data['department']
    
    if 'section' in data:
        employee.section = data['section']
    
    if 'role' in data:
        employee.role = data['role']
    
    if 'is_active' in data:
        employee.is_active = data['is_active']
    
    db.session.commit()
    return jsonify(employee.to_dict()), 200

@employee_bp.route('/<int:employee_id>', methods=['DELETE'])
@role_required('admin')
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    employee.is_active = False
    db.session.commit()
    return jsonify({'message': 'Employee deactivated successfully'}), 200