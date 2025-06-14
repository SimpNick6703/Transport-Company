from flask import render_template, request, redirect, url_for, flash, jsonify
from app.routes import rental_bp
from app import db
from app.models import Rental, Vehicle, Customer
from datetime import datetime, timedelta

@rental_bp.route('/')
def list_rentals():
    """List all rentals"""
    rentals = Rental.query.all()
    return render_template('rentals/index.html', rentals=rentals)

@rental_bp.route('/active')
def active_rentals():
    """List active rentals"""
    rentals = Rental.query.filter_by(rental_status='active').all()
    return render_template('rentals/active.html', rentals=rentals)

@rental_bp.route('/<int:id>')
def view_rental(id):
    """View rental details"""
    rental = Rental.query.get_or_404(id)
    return render_template('rentals/view.html', rental=rental)

@rental_bp.route('/create', methods=['GET', 'POST'])
def create_rental():
    """Create a new rental"""
    if request.method == 'POST':
        # Get form data
        vehicle_id = request.form.get('vehicle_id')
        customer_id = request.form.get('customer_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        start_mileage = request.form.get('start_mileage')
        
        # Get vehicle info for rate
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle or vehicle.status != 'available':
            flash('Vehicle is not available for rental!', 'error')
            return redirect(url_for('rental.create_rental'))
            
        # Create new rental
        rental = Rental(
            vehicle_id=vehicle_id,
            customer_id=customer_id,
            start_date=datetime.strptime(start_date, '%Y-%m-%dT%H:%M'),
            end_date=datetime.strptime(end_date, '%Y-%m-%dT%H:%M'),
            start_mileage=start_mileage,
            daily_rate=vehicle.daily_rate,
            rental_status='booked'
        )

        # Update vehicle status
        vehicle.status = 'rented'
        
        # Save to database
        db.session.add(rental)
        db.session.commit()
        
        flash('Rental created successfully!', 'success')
        return redirect(url_for('rental.list_rentals'))    # Get available vehicles and customers for the form
    vehicles = Vehicle.query.filter_by(status='available').all()
    customers = Customer.query.all()
    today = datetime.now().date()
    
    return render_template('rentals/create.html', 
                         vehicles=vehicles, 
                         customers=customers, 
                         today=today,
                         timedelta=timedelta)

@rental_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_rental(id):
    """Update rental details"""
    rental = Rental.query.get_or_404(id)
    
    if request.method == 'POST':
        # Update rental details
        new_status = request.form.get('rental_status')
        
        if rental.rental_status != 'completed' and new_status == 'completed':
            # Handle vehicle return
            rental.return_date = datetime.utcnow()
            rental.end_mileage = request.form.get('end_mileage')
            
            # Calculate total amount based on days and rate
            if rental.return_date and rental.start_date:
                days = (rental.return_date - rental.start_date).days + 1  # Include last day
                rental.total_amount = days * rental.daily_rate
            
            # Update vehicle status
            vehicle = Vehicle.query.get(rental.vehicle_id)
            if vehicle:
                vehicle.status = 'available'
                vehicle.mileage = rental.end_mileage
        
        rental.rental_status = new_status
        rental.payment_status = request.form.get('payment_status')
        rental.notes = request.form.get('notes')
        rental.updated_at = datetime.utcnow()
        
        # Save changes
        db.session.commit()
        
        flash('Rental updated successfully!', 'success')
        return redirect(url_for('rental.view_rental', id=rental.id))
    
    return render_template('rentals/update.html', rental=rental)

@rental_bp.route('/<int:id>/cancel', methods=['POST'])
def cancel_rental(id):
    """Cancel a rental"""
    rental = Rental.query.get_or_404(id)
    
    # Only allow cancellation if not already active
    if rental.rental_status not in ['active', 'completed']:
        rental.rental_status = 'canceled'
        
        # Update vehicle status if it was set to rented
        vehicle = Vehicle.query.get(rental.vehicle_id)
        if vehicle and vehicle.status == 'rented':
            vehicle.status = 'available'
        
        db.session.commit()
        flash('Rental cancelled successfully!', 'success')
    else:
        flash('Cannot cancel an active or completed rental!', 'error')
        
    return redirect(url_for('rental.list_rentals'))