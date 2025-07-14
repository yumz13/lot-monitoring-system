from src.models import db, Area, Process, Customer, Employee, DefectCode, PartNumber
from src.app import create_app

app = create_app()

def seed_database():
    with app.app_context():
        # Seed Areas
        areas = [
            Area(name='VCM-1', description='Voice Coil Motor Area 1'),
            Area(name='VCM-2', description='Voice Coil Motor Area 2'),
            Area(name='VCM-3', description='Voice Coil Motor Area 3'),
            Area(name='VCS-1', description='Voice Coil Speaker Area 1'),
            Area(name='VCS-2', description='Voice Coil Speaker Area 2')
        ]
        db.session.bulk_save_objects(areas)
        
        # Seed Processes
        processes = [
            Process(name='Material Preparation', order_sequence=1),
            Process(name='Assembly', order_sequence=2),
            Process(name='Assembly Inspection', order_sequence=3),
            Process(name='Oven', order_sequence=4),
            Process(name='QC/QA Inspection', order_sequence=5)
        ]
        db.session.bulk_save_objects(processes)
        
        # Seed more data...
        
        db.session.commit()
        print("Database seeded successfully")

if __name__ == '__main__':
    seed_database()