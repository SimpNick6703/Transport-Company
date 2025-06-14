from app import db
from datetime import datetime

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(20), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)  # car, bus, truck, etc.
    model = db.Column(db.String(100), nullable=False)  # Ambassador, Tata Sumo, Maruti Omni, etc.
    year = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Float, nullable=False)  # passenger capacity or cargo capacity in tons
    
    # Enhanced pricing structure
    daily_rate = db.Column(db.Float, nullable=False)  # rental rate per day (legacy)
    hourly_rate = db.Column(db.Float, nullable=False, default=0.0)  # rate per hour
    per_km_rate = db.Column(db.Float, nullable=False, default=0.0)  # rate per kilometer
    
    # AC/Non-AC categorization
    has_ac = db.Column(db.Boolean, nullable=False, default=False)  # True for AC, False for Non-AC
    
    # Vehicle characteristics
    fuel_type = db.Column(db.String(20), nullable=False, default='Petrol')  # Petrol, Diesel, CNG
    transmission = db.Column(db.String(20), nullable=False, default='Manual')  # Manual, Automatic
    
    # Operational details
    status = db.Column(db.String(20), nullable=False, default='available')  # available, rented, maintenance
    location = db.Column(db.String(100), nullable=True)  # current location of the vehicle
    mileage = db.Column(db.Integer, nullable=False, default=0)
    last_maintenance_date = db.Column(db.DateTime, nullable=True)
    
    # Additional business rules
    minimum_rental_hours = db.Column(db.Integer, nullable=False, default=4)  # minimum 4-hour rental
    night_charge_multiplier = db.Column(db.Float, nullable=False, default=1.25)  # 25% extra for night rentals
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with rentals
    rentals = db.relationship('Rental', back_populates='vehicle', lazy='dynamic')
    
    @property
    def ac_status(self):
        """Return AC/Non-AC status as string"""
        return "AC" if self.has_ac else "Non-AC"
    
    @property
    def display_name(self):
        """Return formatted display name with AC status"""
        return f"{self.model} ({self.ac_status})"
    
    def calculate_rental_cost(self, hours, kilometers, is_night_rental=False):
        """Calculate rental cost based on hours, kilometers, and time"""
        # Ensure minimum rental hours
        actual_hours = max(hours, self.minimum_rental_hours)
        
        # Calculate base cost
        hourly_cost = actual_hours * self.hourly_rate
        km_cost = kilometers * self.per_km_rate
        base_cost = hourly_cost + km_cost
        
        # Apply night charge if applicable
        if is_night_rental:
            base_cost *= self.night_charge_multiplier
            
        return round(base_cost, 2)
    
    def __repr__(self):
        return f"<Vehicle {self.registration_number} - {self.display_name}>"