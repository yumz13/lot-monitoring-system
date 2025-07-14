import uuid
from datetime import datetime

def generate_unique_id(prefix=''):
    """Generate a unique ID with optional prefix"""
    return f"{prefix}{str(uuid.uuid4())[:8]}"

def format_timestamp(timestamp):
    """Format datetime object to readable string"""
    return timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else None