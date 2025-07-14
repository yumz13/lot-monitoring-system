from datetime import datetime
import uuid
from src.models import db, LotTraveler, LotProcessLog

class LotService:
    @staticmethod
    def generate_lot_number():
        """Generate a unique lot number based on date and sequence"""
        today = datetime.now().strftime('%Y%m%d')
        last_lot = LotTraveler.query.filter(
            LotTraveler.lot_number.like(f'{today}%')
        ).order_by(LotTraveler.id.desc()).first()
        
        sequence = int(last_lot.lot_number[-4:]) + 1 if last_lot else 1
        return f"{today}{sequence:04d}"

    @staticmethod
    def create_lot_traveler(area_id, customer_id, part_number_id, quantity, employee_id, **kwargs):
        """Create a new lot traveler with all required fields"""
        try:
            # Generate unique identifiers
            lot_number = LotService.generate_lot_number()
            card_number = f"LTS-{str(uuid.uuid4())[:8]}"
            qr_code = f"QR-{str(uuid.uuid4())[:12]}"
            
            lot = LotTraveler(
                lot_number=lot_number,
                card_number=card_number,
                qr_code=qr_code,
                area_id=area_id,
                customer_id=customer_id,
                part_number_id=part_number_id,
                production_date=datetime.utcnow().date(),
                quantity=quantity,
                material_input_length=kwargs.get('material_length'),
                material_input_weight=kwargs.get('material_weight'),
                status='active'
            )
            
            db.session.add(lot)
            db.session.commit()
            
            # Log process start
            process_log = LotProcessLog(
                lot_traveler_id=lot.id,
                process_id=1,  # Material Prep
                employee_id=employee_id,
                action='start'
            )
            db.session.add(process_log)
            db.session.commit()
            
            return lot, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def log_process_action(lot_id, process_id, employee_id, action):
        """Log a process action (start/complete) for a lot"""
        try:
            log = LotProcessLog(
                lot_traveler_id=lot_id,
                process_id=process_id,
                employee_id=employee_id,
                action=action
            )
            
            db.session.add(log)
            
            # Update lot's current process if completing
            if action == 'complete':
                lot = LotTraveler.query.get(lot_id)
                next_process = Process.query.filter(
                    Process.order_sequence > lot.current_process.order_sequence
                ).order_by(Process.order_sequence).first()
                
                if next_process:
                    lot.current_process_id = next_process.id
            
            db.session.commit()
            return log, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)