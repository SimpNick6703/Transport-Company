from flask import Blueprint

# Create blueprints for different parts of the application
main_bp = Blueprint('main', __name__)
vehicle_bp = Blueprint('vehicle', __name__, url_prefix='/vehicles')
customer_bp = Blueprint('customer', __name__, url_prefix='/customers')
rental_bp = Blueprint('rental', __name__, url_prefix='/rentals')

# Import routes to register them with blueprints
from app.routes import main_routes, vehicle_routes, customer_routes, rental_routes