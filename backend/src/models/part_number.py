from datetime import datetime
from src.models import db

class PartNumber(db.Model):
    __tablename__ = 'part_numbers'
    
    id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String(100), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    description = db.Column(db.String(200))
    oven_program = db.Column(db.String(50))  # Program 1, Program 2, etc.
    oven_steps = db.Column(db.String(50))    # 1-STEP, 3-STEPS, 4-STEPS, etc.
    oven_details = db.Column(db.Text)        # JSON string of step details
    notes = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lot_travelers = db.relationship('LotTraveler', backref='part_number', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'part_number': self.part_number,
            'customer_id': self.customer_id,
            'description': self.description,
            'oven_program': self.oven_program,
            'oven_steps': self.oven_steps,
            'oven_details': self.oven_details,
            'notes': self.notes,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }