from datetime import datetime, timedelta
from src.models import db, OvenLog, LotTraveler
import json

class OvenService:
    OVEN_MATRIX = {
        "PIONEER TVC7695 C/PH": {"program": "Program 1", "steps": "1-STEP", "details": ["Step: 190°C → 30 min"]},
        # ... (other oven configurations from earlier)
    }

    @staticmethod
    def load_to_oven(lot_traveler_id, employee_id, oven_number, layer_number):
        lot = LotTraveler.query.get(lot_traveler_id)
        if not lot:
            return None, "Lot not found"
        
        part_number = f"{lot.customer.name.upper()} {lot.part_number.part_number}"
        config = OvenService.OVEN_MATRIX.get(part_number)
        if not config:
            return None, "Oven configuration not found for this part number"
        
        # Check if oven layer is available
        existing = OvenLog.query.filter_by(
            oven_number=oven_number,
            layer_number=layer_number,
            status='loaded'
        ).first()
        if existing:
            return None, "Oven layer is already occupied"
        
        # Calculate completion time
        total_minutes = sum(int(step.split('→')[1].strip().split(' ')[0]) 
                          for step in config['details'] if '→' in step)
        completion_time = datetime.utcnow() + timedelta(minutes=total_minutes)
        
        log = OvenLog(
            lot_traveler_id=lot.id,
            employee_id=employee_id,
            oven_number=oven_number,
            layer_number=layer_number,
            action='load',
            program_name=config['program'],
            step_details=json.dumps(config['details']),
            load_timestamp=datetime.utcnow(),
            expected_completion=completion_time,
            status='loaded'
        )
        
        db.session.add(log)
        db.session.commit()
        return log.to_dict(), None

    @staticmethod
    def get_oven_status(oven_number=None):
        query = OvenLog.query.filter_by(status='loaded')
        if oven_number:
            query = query.filter_by(oven_number=oven_number)
        
        logs = query.all()
        status = {}
        
        for log in logs:
            if log.oven_number not in status:
                status[log.oven_number] = []
            
            remaining = (log.expected_completion - datetime.utcnow()).total_seconds() / 60
            status[log.oven_number].append({
                'layer': log.layer_number,
                'lot_number': log.lot_traveler.lot_number,
                'program': log.program_name,
                'remaining_minutes': max(0, round(remaining, 1)),
                'details': json.loads(log.step_details)
            })
        
        return status