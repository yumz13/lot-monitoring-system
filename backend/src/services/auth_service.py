import uuid
from datetime import datetime, timedelta
from src.models import db, Employee, LoginSession
from src.utils.helpers import verify_password_hash
from flask import current_app
import jwt

class AuthService:
    @staticmethod
    def login_employee(card_number, area_id, process_id):
        employee = Employee.query.filter_by(card_number=card_number, is_active=True).first()
        if not employee:
            return None, "Employee not found or inactive"
        
        # Create session
        session_token = str(uuid.uuid4())
        session = LoginSession(
            employee_id=employee.id,
            process_id=process_id,
            area_id=area_id,
            session_token=session_token
        )
        
        db.session.add(session)
        db.session.commit()
        
        # Generate JWT token
        token = jwt.encode({
            'employee_id': employee.id,
            'session_token': session_token,
            'role': employee.role,
            'exp': datetime.utcnow() + timedelta(hours=8)
        }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        return {
            'token': token,
            'employee': employee.to_dict(),
            'session': session.to_dict()
        }, None

    @staticmethod
    def logout_employee(session_token):
        session = LoginSession.query.filter_by(session_token=session_token, is_active=True).first()
        if not session:
            return False, "Session not found or already logged out"
        
        session.logout_timestamp = datetime.utcnow()
        session.is_active = False
        db.session.commit()
        return True, None

    @staticmethod
    def validate_token(token):
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            session = LoginSession.query.filter_by(
                session_token=payload['session_token'],
                is_active=True
            ).first()
            
            if not session:
                return None, "Invalid session"
                
            return payload, None
        except jwt.ExpiredSignatureError:
            return None, "Token expired"
        except jwt.InvalidTokenError:
            return None, "Invalid token"