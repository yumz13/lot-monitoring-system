from datetime import datetime
import uuid
from src.models import db

class LotTraveler(db.Model):
    __tablename__ = 'lot_travelers'
    
    id = db.Column(db.Integer, primary_key=True)
    lot_number = db.Column(db.String(100), nullable=False, unique=True)
    card_number = db.Column(db.String(50), unique=True)
    qr_code = db.Column(db.String(200), unique=True)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    part_number_id = db.Column(db.Integer, db.ForeignKey('part_numbers.id'), nullable=False)
    production_date = db.Column(db.Date, nullable=False)
    machine_number = db.Column(db.String(50))
    line_number = db.Column(db.String(50))
    quantity = db.Column(db.Integer, nullable=False)
    material_input_length = db.Column(db.Float)
    material_input_weight = db.Column(db.Float)
    current_process_id = db.Column(db.Integer, db.ForeignKey('processes.id'))
    status = db.Column(db.String(50), default='active')  # active, completed, on_hold
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    process_logs = db.relationship('LotProcessLog', backref='lot_traveler', lazy=True)
    defect_logs = db.relationship('DefectLog', backref='lot_traveler', lazy=True)
    oven_logs = db.relationship('OvenLog', backref='lot_traveler', lazy=True)
    
    def generate_unique_identifiers(self):
        """Generate unique card number and QR code"""
        if not self.card_number:
            self.card_number = f"LTS{str(uuid.uuid4())[:8].upper()}"
        if not self.qr_code:
            self.qr_code = f"QR{str(uuid.uuid4())[:12].upper()}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'lot_number': self.lot_number,
            'card_number': self.card_number,
            'qr_code': self.qr_code,
            'area_id': self.area_id,
            'customer_id': self.customer_id,
            'part_number_id': self.part_number_id,
            'production_date': self.production_date.isoformat(),
            'machine_number': self.machine_number,
            'line_number': self.line_number,
            'quantity': self.quantity,
            'material_input_length': self.material_input_length,
            'material_input_weight': self.material_input_weight,
            'current_process_id': self.current_process_id,
            'status': self.status,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }