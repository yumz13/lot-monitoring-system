from datetime import datetime
from src.models import db

class LotProcessLog(db.Model):
    __tablename__ = 'lot_process_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    lot_traveler_id = db.Column(db.Integer, db.ForeignKey('lot_travelers.id'), nullable=False)
    process_id = db.Column(db.Integer, db.ForeignKey('processes.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # start, complete, pause, resume
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'lot_traveler_id': self.lot_traveler_id,
            'process_id': self.process_id,
            'employee_id': self.employee_id,
            'action': self.action,
            'timestamp': self.timestamp.isoformat(),
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }