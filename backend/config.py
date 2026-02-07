"""
Configuration management for the application.
Loads environment variables and provides centralized config access.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    
    # Database Configuration
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:password@localhost:5432/google_ads_db'
    )
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    
    # Google Ads API Configuration
    GOOGLE_ADS_DEVELOPER_TOKEN = os.getenv('GOOGLE_ADS_DEVELOPER_TOKEN', '')
    GOOGLE_ADS_CLIENT_ID = os.getenv('GOOGLE_ADS_CLIENT_ID', '')
    GOOGLE_ADS_CLIENT_SECRET = os.getenv('GOOGLE_ADS_CLIENT_SECRET', '')
    GOOGLE_ADS_REFRESH_TOKEN = os.getenv('GOOGLE_ADS_REFRESH_TOKEN', '')
    GOOGLE_ADS_LOGIN_CUSTOMER_ID = os.getenv('GOOGLE_ADS_LOGIN_CUSTOMER_ID', '')
    GOOGLE_ADS_CUSTOMER_ID = os.getenv('GOOGLE_ADS_CUSTOMER_ID', '')
    
    @staticmethod
    def validate_google_ads_config():
        """Validate that all required Google Ads credentials are present."""
        required_fields = [
            'GOOGLE_ADS_DEVELOPER_TOKEN',
            'GOOGLE_ADS_CLIENT_ID',
            'GOOGLE_ADS_CLIENT_SECRET',
            'GOOGLE_ADS_REFRESH_TOKEN',
            'GOOGLE_ADS_LOGIN_CUSTOMER_ID',
            'GOOGLE_ADS_CUSTOMER_ID',
        ]
        
        missing = []
        for field in required_fields:
            if not getattr(Config, field):
                missing.append(field)
        
        if missing:
            return False, missing
        return True, []
    
    @staticmethod
    def get_google_ads_config():
        """Get Google Ads configuration as a dictionary."""
        return {
            'developer_token': Config.GOOGLE_ADS_DEVELOPER_TOKEN,
            'client_id': Config.GOOGLE_ADS_CLIENT_ID,
            'client_secret': Config.GOOGLE_ADS_CLIENT_SECRET,
            'refresh_token': Config.GOOGLE_ADS_REFRESH_TOKEN,
            'login_customer_id': Config.GOOGLE_ADS_LOGIN_CUSTOMER_ID,
            'customer_id': Config.GOOGLE_ADS_CUSTOMER_ID,
        }
