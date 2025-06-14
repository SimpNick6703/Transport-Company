from app import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    driving_license_number = db.Column(db.String(50), unique=True, nullable=False)
    license_expiry_date = db.Column(db.Date, nullable=False)
    customer_type = db.Column(db.String(20), nullable=False, default='individual')  # individual or corporate
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with rentals
    rentals = db.relationship('Rental', back_populates='customer', lazy='dynamic')
    
    def __repr__(self):
        return f"<Customer {self.id} - {self.first_name} {self.last_name}>"