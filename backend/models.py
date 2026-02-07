"""
Database models for the application.
Defines the Campaign model with all necessary fields.
"""

import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Campaign(db.Model):
    """Campaign model representing a marketing campaign."""
    
    __tablename__ = 'campaigns'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Campaign basic information
    name = db.Column(db.String(255), nullable=False)
    objective = db.Column(db.String(50))  # SALES, LEADS, WEBSITE_TRAFFIC, etc.
    campaign_type = db.Column(db.String(50), default='DEMAND_GEN')
    
    # Budget and dates
    daily_budget = db.Column(db.Integer)  # Budget in micros (e.g., 50000 = $50)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # Status tracking
    status = db.Column(db.String(20), default='DRAFT')  # DRAFT, PUBLISHED, PAUSED
    google_campaign_id = db.Column(db.String(100), unique=True, nullable=True)
    
    # Ad group and creative details
    ad_group_name = db.Column(db.String(255))
    ad_headline = db.Column(db.String(500))
    ad_description = db.Column(db.Text)
    asset_url = db.Column(db.String(500))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Campaign {self.name} ({self.status})>'
    
    def to_dict(self):
        """Convert campaign to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'objective': self.objective,
            'campaign_type': self.campaign_type,
            'daily_budget': self.daily_budget,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'google_campaign_id': self.google_campaign_id,
            'ad_group_name': self.ad_group_name,
            'ad_headline': self.ad_headline,
            'ad_description': self.ad_description,
            'asset_url': self.asset_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @staticmethod
    def validate_campaign_data(data):
        """Validate campaign data before creation/update."""
        errors = []
        
        # Required fields
        if not data.get('name'):
            errors.append('Campaign name is required')
        
        # Budget validation
        if data.get('daily_budget') is not None:
            try:
                budget = int(data['daily_budget'])
                if budget < 0:
                    errors.append('Daily budget must be positive')
            except (ValueError, TypeError):
                errors.append('Daily budget must be a valid number')
        
        # Date validation
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date:
            try:
                from datetime import datetime
                start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                if end < start:
                    errors.append('End date must be after start date')
            except (ValueError, AttributeError):
                errors.append('Invalid date format')
        
        return errors
