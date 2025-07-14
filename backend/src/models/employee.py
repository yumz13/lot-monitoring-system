from datetime import datetime
from src.models import db

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.String(50), nullable=False, unique=True)
    card_number = db.Column(db.String(50), nullable=False, unique=True)
    department = db.Column(db.String(100))
    section = db.Column(db.String(100))
    role = db.Column(db.String(50), default='operator')  # operator, inspector, technician, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lot_process_logs = db.relationship('LotProcessLog', backref='employee', lazy=True)
    login_sessions = db.relationship('LoginSession', backref='employee', lazy=True)
    defect_logs = db.relationship('DefectLog', backref='employee', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'employee_id': self.employee_id,
            'card_number': self.card_number,
            'department': self.department,
            'section': self.section,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }