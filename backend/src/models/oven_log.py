from datetime import datetime
from src.models import db

class OvenLog(db.Model):
    __tablename__ = 'oven_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    lot_traveler_id = db.Column(db.Integer, db.ForeignKey('lot_travelers.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    oven_number = db.Column(db.Integer, nullable=False)  # 1-10
    layer_number = db.Column(db.Integer, nullable=False)  # 1-15
    action = db.Column(db.String(50), nullable=False)  # load, unload, emergency_stop
    program_name = db.Column(db.String(50))
    step_details = db.Column(db.Text)  # JSON string of step details
    load_timestamp = db.Column(db.DateTime)
    unload_timestamp = db.Column(db.DateTime)
    expected_completion = db.Column(db.DateTime)
    actual_completion = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='loaded')  # loaded, in_progress, completed, emergency_stopped
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'lot_traveler_id': self.lot_traveler_id,
            'employee_id': self.employee_id,
            'oven_number': self.oven_number,
            'layer_number': self.layer_number,
            'action': self.action,
            'program_name': self.program_name,
            'step_details': self.step_details,
            'load_timestamp': self.load_timestamp.isoformat() if self.load_timestamp else None,
            'unload_timestamp': self.unload_timestamp.isoformat() if self.unload_timestamp else None,
            'expected_completion': self.expected_completion.isoformat() if self.expected_completion else None,
            'actual_completion': self.actual_completion.isoformat() if self.actual_completion else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }