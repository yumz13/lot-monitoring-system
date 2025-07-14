from flask import Blueprint, request, jsonify
from src.models import db, LotTraveler, LotProcessLog, Process
from src.services.lot_service import LotService
from src.services.qr_service import QRService
from src.utils.decorators import role_required, validate_json

lot_traveler_bp = Blueprint('lot_traveler', __name__)

@lot_traveler_bp.route('/', methods=['POST'])
@role_required('operator')
@validate_json({
    'area_id': int,
    'customer_id': int,
    'part_number_id': int,
    'quantity': int,
    'employee_id': int
})
def create_lot_traveler():
    data = request.get_json()
    lot, error = LotService.create_lot_traveler(
        data['area_id'],
        data['customer_id'],
        data['part_number_id'],
        data['quantity'],
        data['employee_id'],
        material_length=data.get('material_length'),
        material_weight=data.get('material_weight')
    )
    
    if error:
        return jsonify({'error': error}), 400
    return jsonify(lot.to_dict()), 201

@lot_traveler_bp.route('/<int:lot_id>', methods=['GET'])
def get_lot_traveler(lot_id):
    lot = LotTraveler.query.get_or_404(lot_id)
    return jsonify(lot.to_dict()), 200

@lot_traveler_bp.route('/process-log', methods=['POST'])
@role_required('operator')
@validate_json({
    'lot_id': int,
    'process_id': int,
    'employee_id': int,
    'action': str
})
def log_process_action():
    data = request.get_json()
    log, error = LotService.log_process_action(
        data['lot_id'],
        data['process_id'],
        data['employee_id'],
        data['action']
    )
    
    if error:
        return jsonify({'error': error}), 400
    return jsonify(log.to_dict()), 201

@lot_traveler_bp.route('/qr-code/<int:lot_id>', methods=['GET'])
def generate_qr_code(lot_id):
    result, error = QRService.generate_qr_code(lot_id)
    if error:
        return jsonify({'error': error}), 400
    return jsonify(result), 200