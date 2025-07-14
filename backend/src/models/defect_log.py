from datetime import datetime
from src.models import db

class DefectLog(db.Model):
    __tablename__ = 'defect_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    lot_traveler_id = db.Column(db.Integer, db.ForeignKey('lot_travelers.id'), nullable=False)
    process_id = db.Column(db.Integer, db.ForeignKey('processes.id'), nullable=False)
    defect_code_id = db.Column(db.Integer, db.ForeignKey('defect_codes.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'lot_traveler_id': self.lot_traveler_id,
            'process_id': self.process_id,
            'defect_code_id': self.defect_code_id,
            'employee_id': self.employee_id,
            'quantity': self.quantity,
            'timestamp': self.timestamp.isoformat(),
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }