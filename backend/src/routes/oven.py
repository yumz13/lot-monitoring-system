from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.models import db, OvenLog, LotTraveler
from src.services.oven_service import OvenService
from src.utils.decorators import role_required
import json

oven_bp = Blueprint('oven', __name__)

@oven_bp.route('/load', methods=['POST'])
@role_required('technician')
def load_oven():
    data = request.get_json()
    required_fields = ['lot_traveler_id', 'employee_id', 'oven_number', 'layer_number']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    result, error = OvenService.load_to_oven(
        data['lot_traveler_id'],
        data['employee_id'],
        data['oven_number'],
        data['layer_number']
    )
    
    if error:
        return jsonify({'error': error}), 400
    return jsonify(result), 201

@oven_bp.route('/unload', methods=['POST'])
@role_required('technician')
def unload_oven():
    data = request.get_json()
    if not all(field in data for field in ['lot_traveler_id', 'employee_id']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Find active oven log
    oven_log = OvenLog.query.filter_by(
        lot_traveler_id=data['lot_traveler_id'],
        status='loaded'
    ).first()
    
    if not oven_log:
        return jsonify({'error': 'No active oven session found'}), 404
    
    # Update oven log
    oven_log.action = 'unload'
    oven_log.unload_timestamp = datetime.utcnow()
    oven_log.actual_completion = datetime.utcnow()
    oven_log.status = 'completed'
    oven_log.employee_id = data['employee_id']
    
    db.session.commit()
    return jsonify(oven_log.to_dict()), 200

@oven_bp.route('/status', methods=['GET'])
def get_oven_status():
    oven_number = request.args.get('oven_number')
    status = OvenService.get_oven_status(oven_number)
    return jsonify(status), 200

@oven_bp.route('/emergency-stop', methods=['POST'])
@role_required('technician')
def emergency_stop():
    data = request.get_json()
    if not all(field in data for field in ['oven_number', 'employee_id']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Find all active logs for this oven
    active_logs = OvenLog.query.filter_by(
        oven_number=data['oven_number'],
        status='loaded'
    ).all()
    
    # Update all active logs
    for log in active_logs:
        log.status = 'emergency_stopped'
        log.actual_completion = datetime.utcnow()
        log.notes = f"Emergency stop by employee {data['employee_id']}"
    
    db.session.commit()
    return jsonify({
        'message': f'Emergency stop executed for oven {data["oven_number"]}',
        'affected_lots': len(active_logs)
    }), 200