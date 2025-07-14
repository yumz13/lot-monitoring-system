import qrcode
import os
from io import BytesIO
from datetime import datetime
from src.models import LotTraveler
from src.app import current_app

class QRService:
    @staticmethod
    def generate_qr_code(lot_traveler_id):
        lot = LotTraveler.query.get(lot_traveler_id)
        if not lot:
            return None, "Lot traveler not found"
        
        # Create QR code data
        qr_data = f"LOT:{lot.lot_number}|PN:{lot.part_number.part_number}|QTY:{lot.quantity}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to static folder
        qr_folder = os.path.join(current_app.static_folder, 'qr_codes')
        os.makedirs(qr_folder, exist_ok=True)
        
        filename = f"qr_{lot.lot_number}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        filepath = os.path.join(qr_folder, filename)
        img.save(filepath)
        
        # Update lot with QR code filename
        lot.qr_code = filename
        db.session.commit()
        
        return {
            'qr_code': filename,
            'qr_data': qr_data,
            'qr_url': f"/static/qr_codes/{filename}"
        }, None