from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from src.models import db, LotTraveler, LotProcessLog, DefectLog, Process

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/overview', methods=['GET'])
def get_dashboard_overview():
    # Get filter parameters
    date_filter = request.args.get('filter', 'daily')
    
    # Calculate date range
    end_dt = datetime.utcnow()
    if date_filter == 'daily':
        start_dt = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    elif date_filter == 'weekly':
        start_dt = end_dt - timedelta(days=7)
    elif date_filter == 'monthly':
        start_dt = end_dt - timedelta(days=30)
    else:
        start_dt = end_dt - timedelta(days=1)

    # Get production data
    lots = LotTraveler.query.filter(
        and_(
            LotTraveler.created_at >= start_dt,
            LotTraveler.created_at < end_dt,
            LotTraveler.is_active == True
        )
    ).all()

    # Get defect data
    defects = DefectLog.query.filter(
        and_(
            DefectLog.timestamp >= start_dt,
            DefectLog.timestamp < end_dt
        )
    ).all()

    # Calculate metrics
    total_lots = len(lots)
    completed_lots = len([lot for lot in lots if lot.status == 'completed'])
    active_lots = len([lot for lot in lots if lot.status == 'active'])
    total_defects = sum([defect.quantity for defect in defects])
    defect_rate = (total_defects / total_lots * 100) if total_lots > 0 else 0

    return jsonify({
        'summary': {
            'total_lots': total_lots,
            'completed_lots': completed_lots,
            'active_lots': active_lots,
            'total_defects': total_defects,
            'defect_rate': round(defect_rate, 2)
        },
        'date_range': {
            'start': start_dt.isoformat(),
            'end': end_dt.isoformat(),
            'filter': date_filter
        }
    }), 200

@dashboard_bp.route('/process-performance', methods=['GET'])
def get_process_performance():
    processes = Process.query.filter_by(is_active=True).order_by(Process.order_sequence).all()
    performance_data = []
    
    for process in processes:
        start_logs = LotProcessLog.query.filter(
            LotProcessLog.process_id == process.id,
            LotProcessLog.action == 'start'
        ).count()
        
        complete_logs = LotProcessLog.query.filter(
            LotProcessLog.process_id == process.id,
            LotProcessLog.action == 'complete'
        ).count()
        
        performance_data.append({
            'process_name': process.name,
            'lots_started': start_logs,
            'lots_completed': complete_logs,
            'completion_rate': round((complete_logs / start_logs * 100), 2) if start_logs else 0
        })
    
    return jsonify(performance_data), 200