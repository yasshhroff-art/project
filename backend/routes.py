"""
API routes for campaign management.
Defines all REST endpoints for CRUD operations and Google Ads publishing.
"""

from flask import Blueprint, request, jsonify
from models import db, Campaign
from google_ads_service import GoogleAdsService
from config import Config
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/campaigns', methods=['GET'])
def get_campaigns():
    """Get all campaigns from the database."""
    try:
        campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
        return jsonify({
            'campaigns': [campaign.to_dict() for campaign in campaigns]
        }), 200
    except Exception as e:
        logger.error(f"Error fetching campaigns: {str(e)}")
        return jsonify({'error': 'Failed to fetch campaigns'}), 500


@api.route('/campaigns/<campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    """Get a specific campaign by ID."""
    try:
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        return jsonify(campaign.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching campaign: {str(e)}")
        return jsonify({'error': 'Failed to fetch campaign'}), 500


@api.route('/campaigns', methods=['POST'])
def create_campaign():
    """Create a new campaign in the local database."""
    try:
        data = request.get_json()
        
        # Validate input data
        validation_errors = Campaign.validate_campaign_data(data)
        if validation_errors:
            return jsonify({
                'error': 'Validation failed',
                'details': validation_errors
            }), 400
        
        # Create new campaign
        campaign = Campaign(
            name=data.get('name'),
            objective=data.get('objective'),
            campaign_type=data.get('campaign_type', 'DEMAND_GEN'),
            daily_budget=data.get('daily_budget'),
            start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else None,
            end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
            ad_group_name=data.get('ad_group_name'),
            ad_headline=data.get('ad_headline'),
            ad_description=data.get('ad_description'),
            asset_url=data.get('asset_url'),
            status='DRAFT'
        )
        
        db.session.add(campaign)
        db.session.commit()
        
        logger.info(f"Created campaign: {campaign.id}")
        return jsonify({
            'message': 'Campaign created successfully',
            'campaign': campaign.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating campaign: {str(e)}")
        return jsonify({'error': f'Failed to create campaign: {str(e)}'}), 500


@api.route('/campaigns/<campaign_id>', methods=['PUT'])
def update_campaign(campaign_id):
    """Update an existing campaign."""
    try:
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        # Don't allow updating published campaigns
        if campaign.status == 'PUBLISHED':
            return jsonify({
                'error': 'Cannot update published campaign. Create a new one instead.'
            }), 400
        
        data = request.get_json()
        
        # Validate input data
        validation_errors = Campaign.validate_campaign_data(data)
        if validation_errors:
            return jsonify({
                'error': 'Validation failed',
                'details': validation_errors
            }), 400
        
        # Update fields
        if 'name' in data:
            campaign.name = data['name']
        if 'objective' in data:
            campaign.objective = data['objective']
        if 'campaign_type' in data:
            campaign.campaign_type = data['campaign_type']
        if 'daily_budget' in data:
            campaign.daily_budget = data['daily_budget']
        if 'start_date' in data:
            campaign.start_date = datetime.fromisoformat(data['start_date']) if data['start_date'] else None
        if 'end_date' in data:
            campaign.end_date = datetime.fromisoformat(data['end_date']) if data['end_date'] else None
        if 'ad_group_name' in data:
            campaign.ad_group_name = data['ad_group_name']
        if 'ad_headline' in data:
            campaign.ad_headline = data['ad_headline']
        if 'ad_description' in data:
            campaign.ad_description = data['ad_description']
        if 'asset_url' in data:
            campaign.asset_url = data['asset_url']
        
        campaign.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        logger.info(f"Updated campaign: {campaign.id}")
        return jsonify({
            'message': 'Campaign updated successfully',
            'campaign': campaign.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating campaign: {str(e)}")
        return jsonify({'error': f'Failed to update campaign: {str(e)}'}), 500


@api.route('/campaigns/<campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    """Delete a campaign from the database."""
    try:
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        # Warn if deleting published campaign
        if campaign.status == 'PUBLISHED':
            logger.warning(f"Deleting published campaign: {campaign.id}")
        
        db.session.delete(campaign)
        db.session.commit()
        
        logger.info(f"Deleted campaign: {campaign_id}")
        return jsonify({'message': 'Campaign deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting campaign: {str(e)}")
        return jsonify({'error': 'Failed to delete campaign'}), 500


@api.route('/campaigns/<campaign_id>/publish', methods=['POST'])
def publish_campaign(campaign_id):
    """Publish a campaign to Google Ads."""
    try:
        # Get campaign from database
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        # Check if already published
        if campaign.status == 'PUBLISHED':
            return jsonify({
                'error': 'Campaign is already published',
                'google_campaign_id': campaign.google_campaign_id
            }), 400
        
        # Validate Google Ads configuration
        is_valid, missing_fields = Config.validate_google_ads_config()
        if not is_valid:
            return jsonify({
                'error': 'Google Ads configuration incomplete',
                'missing_fields': missing_fields
            }), 500
        
        # Initialize Google Ads service
        google_ads_config = Config.get_google_ads_config()
        ads_service = GoogleAdsService(google_ads_config)
        
        # Prepare campaign data
        campaign_data = {
            'name': campaign.name,
            'objective': campaign.objective,
            'campaign_type': campaign.campaign_type,
            'daily_budget': campaign.daily_budget or 50000,  # Default $50
            'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            'ad_group_name': campaign.ad_group_name or 'Main Ad Group',
            'ad_headline': campaign.ad_headline or 'Default Headline',
            'ad_description': campaign.ad_description or 'Default Description',
            'asset_url': campaign.asset_url
        }
        
        # Publish to Google Ads
        result = ads_service.publish_campaign(campaign_data)
        
        # Update campaign in database
        campaign.google_campaign_id = result['campaign_id']
        campaign.status = 'PUBLISHED'
        campaign.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        logger.info(f"Published campaign {campaign_id} to Google Ads: {result['campaign_id']}")
        
        return jsonify({
            'message': 'Campaign published successfully',
            'google_campaign_id': result['campaign_id'],
            'ad_group_id': result['ad_group_id'],
            'ad_id': result['ad_id'],
            'status': 'PUBLISHED'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error publishing campaign: {str(e)}")
        return jsonify({
            'error': f'Failed to publish campaign: {str(e)}'
        }), 500


@api.route('/campaigns/<campaign_id>/disable', methods=['POST'])
def disable_campaign(campaign_id):
    """Disable (pause) a campaign in Google Ads."""
    try:
        # Get campaign from database
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        # Check if published
        if campaign.status != 'PUBLISHED' or not campaign.google_campaign_id:
            return jsonify({
                'error': 'Campaign is not published to Google Ads'
            }), 400
        
        # Validate Google Ads configuration
        is_valid, missing_fields = Config.validate_google_ads_config()
        if not is_valid:
            return jsonify({
                'error': 'Google Ads configuration incomplete',
                'missing_fields': missing_fields
            }), 500
        
        # Initialize Google Ads service
        google_ads_config = Config.get_google_ads_config()
        ads_service = GoogleAdsService(google_ads_config)
        
        # Disable in Google Ads
        ads_service.disable_campaign(campaign.google_campaign_id)
        
        # Update status in database
        campaign.status = 'PAUSED'
        campaign.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        logger.info(f"Disabled campaign {campaign_id} in Google Ads")
        
        return jsonify({
            'message': 'Campaign disabled successfully',
            'status': 'PAUSED'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error disabling campaign: {str(e)}")
        return jsonify({
            'error': f'Failed to disable campaign: {str(e)}'
        }), 500


@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        
        # Check Google Ads config
        is_valid, missing_fields = Config.validate_google_ads_config()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'google_ads_config': 'valid' if is_valid else 'invalid',
            'missing_config': missing_fields if not is_valid else []
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500
