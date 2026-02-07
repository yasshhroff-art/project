"""
Database initialization script.
Creates all necessary tables in PostgreSQL.
"""

from app import create_app
from models import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    """Initialize the database with all tables."""
    app = create_app()
    
    with app.app_context():
        try:
            # Drop all tables (be careful in production!)
            logger.info("Dropping existing tables...")
            db.drop_all()
            
            # Create all tables
            logger.info("Creating database tables...")
            db.create_all()
            
            logger.info("Database initialized successfully!")
            logger.info("Tables created:")
            logger.info("  - campaigns")
            
            # Print table info
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            for table_name in inspector.get_table_names():
                logger.info(f"\nTable: {table_name}")
                for column in inspector.get_columns(table_name):
                    logger.info(f"  - {column['name']}: {column['type']}")
            
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise


if __name__ == '__main__':
    init_database()
