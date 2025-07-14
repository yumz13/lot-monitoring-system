from datetime import datetime
from src.models import db

class Process(db.Model):
    __tablename__ = 'processes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Material Preparation, Assembly, etc.
    order_sequence = db.Column(db.Integer, nullable=False)  # 1, 2, 3, 4, 5
    description = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lot_process_logs = db.relationship('LotProcessLog', backref='process', lazy=True)
    login_sessions = db.relationship('LoginSession', backref='process', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'order_sequence': self.order_sequence,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }