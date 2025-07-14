from .area import area_bp
from .auth import auth_bp
from .customer import customer_bp
from .dashboard import dashboard_bp
from .defect_code import defect_code_bp
from .employee import employee_bp
from .lot_traveler import lot_traveler_bp
from .oven import oven_bp
from .part_number import part_number_bp
from .process import process_bp

def register_blueprints(app):
    app.register_blueprint(area_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(customer_bp, url_prefix='/api/customers')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(defect_code_bp, url_prefix='/api/defect-codes')
    app.register_blueprint(employee_bp, url_prefix='/api/employees')
    app.register_blueprint(lot_traveler_bp, url_prefix='/api/lot-travelers')
    app.register_blueprint(oven_bp, url_prefix='/api/oven')
    app.register_blueprint(part_number_bp, url_prefix='/api/part-numbers')
    app.register_blueprint(process_bp, url_prefix='/api/processes')