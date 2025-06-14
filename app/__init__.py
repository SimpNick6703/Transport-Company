from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from app.utils.logger import logger

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure SQLite database
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(os.path.dirname(basedir), 'database', 'transport.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'transport-company-secret-key'
    
    # Initialize db with app
    db.init_app(app)
    
    # Register blueprints
    from app.routes import main_bp, vehicle_bp, customer_bp, rental_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(vehicle_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(rental_bp)
    
    # Configure error handling
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """Register error handlers for the Flask app"""
    
    @app.errorhandler(404)
    def page_not_found(e):
        logger.warning(f"Page not found: {e}")
        return "Page not found", 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        logger.error(f"Internal server error: {e}")
        return "Internal server error", 500
    
    @app.errorhandler(Exception)
    def unhandled_exception(e):
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
        return "An unexpected error occurred", 500