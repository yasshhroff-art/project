"""
Main Flask application entry point.
Sets up the Flask app, database, CORS, and routes.
"""

from flask import Flask
from flask_cors import CORS
from models import db
from routes import api
from config import Config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": Config.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(api)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'message': 'Google Ads Campaign Manager API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'campaigns': '/api/campaigns',
                'create_campaign': 'POST /api/campaigns',
                'get_campaign': '/api/campaigns/{id}',
                'update_campaign': 'PUT /api/campaigns/{id}',
                'delete_campaign': 'DELETE /api/campaigns/{id}',
                'publish_campaign': 'POST /api/campaigns/{id}/publish',
                'disable_campaign': 'POST /api/campaigns/{id}/disable'
            }
        }
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Log configuration status
    is_valid, missing = Config.validate_google_ads_config()
    if not is_valid:
        logger.warning(f"Google Ads configuration incomplete. Missing: {missing}")
        logger.warning("Publishing to Google Ads will not work until configuration is complete.")
    else:
        logger.info("Google Ads configuration is valid")
    
    # Run the application
    logger.info("Starting Flask application on http://localhost:5000")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    )
