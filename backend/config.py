import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'pyrites-grill-default-dev-key')
    ADMIN_API_KEY = os.getenv('ADMIN_API_KEY', 'pg-admin-secret-key-123')
    
    # Handle DB URL format compatibility (mysql:// -> mysql+pymysql://)
    db_url = os.getenv('DATABASE_URL', 'sqlite:///pyrites_grill.db')
    if db_url.startswith('mysql://'):
        db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)
        
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_pre_ping': True,
    }
    
    # Restaurant Operating Rules
    RESTAURANT_NAME = "Pyrites Grill"
    OPENING_TIME = "12:00"  # 12:00 PM
    CLOSING_TIME = "23:00"  # 11:00 PM
    SLOT_DURATION_MINUTES = 90  # Each booking lasts 90 mins
    MAX_GUESTS_PER_BOOKING = 12
