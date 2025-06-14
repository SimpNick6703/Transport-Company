from app import db
from datetime import datetime

class Rental(db.Model):
    __tablename__ = 'rentals'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)  # Actual return date
    start_mileage = db.Column(db.Integer, nullable=False)
    end_mileage = db.Column(db.Integer, nullable=True)
    rental_status = db.Column(db.String(20), nullable=False, default='booked')  # booked, active, completed, canceled
    
    # Enhanced pricing fields
    daily_rate = db.Column(db.Float, nullable=False)  # Legacy field, kept for compatibility
    hourly_rate = db.Column(db.Float, nullable=False, default=0.0)  # Rate per hour used
    per_km_rate = db.Column(db.Float, nullable=False, default=0.0)  # Rate per kilometer used
    
    # Rental duration and distance
    total_hours = db.Column(db.Float, nullable=True)  # Actual rental hours
    total_kilometers = db.Column(db.Float, nullable=True)  # Kilometers driven
    
    # Cost breakdown
    hourly_cost = db.Column(db.Float, nullable=True)  # Cost for hours
    km_cost = db.Column(db.Float, nullable=True)  # Cost for kilometers
    night_charge = db.Column(db.Float, nullable=True, default=0.0)  # Additional night charges
    total_amount = db.Column(db.Float, nullable=True)  # Final calculated amount
    
    # Flags
    is_night_rental = db.Column(db.Boolean, nullable=False, default=False)  # True if night rental
    
    payment_status = db.Column(db.String(20), nullable=False, default='pending')  # pending, paid, refunded
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vehicle = db.relationship('Vehicle', back_populates='rentals')
    customer = db.relationship('Customer', back_populates='rentals')
    
    def calculate_total_cost(self):
        """Calculate total rental cost based on hours, kilometers, and night charges"""
        if not self.vehicle:
            return 0.0
            
        # Calculate hours if return date is available
        if self.return_date and self.start_date:
            time_diff = self.return_date - self.start_date
            self.total_hours = round(time_diff.total_seconds() / 3600, 2)
        elif self.end_date and self.start_date:
            time_diff = self.end_date - self.start_date
            self.total_hours = round(time_diff.total_seconds() / 3600, 2)
        else:
            self.total_hours = 0.0
            
        # Calculate kilometers if end mileage is available
        if self.end_mileage and self.start_mileage:
            self.total_kilometers = self.end_mileage - self.start_mileage
        else:
            self.total_kilometers = 0.0
            
        # Use vehicle's calculation method
        self.total_amount = self.vehicle.calculate_rental_cost(
            self.total_hours or 0, 
            self.total_kilometers or 0, 
            self.is_night_rental
        )
        
        # Store rate breakdown
        self.hourly_rate = self.vehicle.hourly_rate
        self.per_km_rate = self.vehicle.per_km_rate
        
        # Calculate cost components
        min_hours = max(self.total_hours or 0, self.vehicle.minimum_rental_hours)
        self.hourly_cost = min_hours * self.hourly_rate
        self.km_cost = (self.total_kilometers or 0) * self.per_km_rate
        
        if self.is_night_rental:
            base_cost = self.hourly_cost + self.km_cost
            self.night_charge = base_cost * (self.vehicle.night_charge_multiplier - 1)
        else:
            self.night_charge = 0.0
            
        return self.total_amount
    
    @property 
    def duration_display(self):
        """Return formatted duration string"""
        if self.total_hours:
            hours = int(self.total_hours)
            minutes = int((self.total_hours - hours) * 60)
            return f"{hours}h {minutes}m"
        return "N/A"
    
    def __repr__(self):
        return f"<Rental {self.id} - Vehicle: {self.vehicle_id}, Customer: {self.customer_id}>"