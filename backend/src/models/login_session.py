from datetime import datetime
from src.models import db

class LoginSession(db.Model):
    __tablename__ = 'login_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    process_id = db.Column(db.Integer, db.ForeignKey('processes.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    login_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    logout_timestamp = db.Column(db.DateTime)
    session_token = db.Column(db.String(200), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'process_id': self.process_id,
            'area_id': self.area_id,
            'login_timestamp': self.login_timestamp.isoformat(),
            'logout_timestamp': self.logout_timestamp.isoformat() if self.logout_timestamp else None,
            'session_token': self.session_token,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }