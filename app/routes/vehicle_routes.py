from flask import render_template, request, redirect, url_for, flash, jsonify
from app.routes import vehicle_bp
from app import db
from app.models import Vehicle, Rental
from datetime import datetime
from app.utils import logger, log_error, log_exception

@vehicle_bp.route('/')
def list_vehicles():
    """List all vehicles"""
    try:
        vehicles = Vehicle.query.all()
        return render_template('vehicles/index.html', vehicles=vehicles)
    except Exception as e:
        log_exception(e, "Error retrieving vehicle list")
        flash('An error occurred while loading vehicles', 'danger')
        return render_template('vehicles/index.html', vehicles=[])

@vehicle_bp.route('/available')
def available_vehicles():
    """List available vehicles for rent"""
    try:
        vehicles = Vehicle.query.filter_by(status='available').all()
        return render_template('vehicles/available.html', vehicles=vehicles)
    except Exception as e:
        log_exception(e, "Error retrieving available vehicles")
        flash('An error occurred while loading available vehicles', 'danger')
        return render_template('vehicles/available.html', vehicles=[])

@vehicle_bp.route('/<int:id>')
def view_vehicle(id):
    """View vehicle details"""
    try:
        vehicle = Vehicle.query.get_or_404(id)
        return render_template('vehicles/view.html', vehicle=vehicle)
    except Exception as e:
        log_exception(e, f"Error retrieving vehicle with ID {id}")
        flash('Vehicle not found or an error occurred', 'danger')
        return redirect(url_for('vehicle.list_vehicles'))

@vehicle_bp.route('/create', methods=['GET', 'POST'])
@log_error(message="Error creating vehicle")
def create_vehicle():
    """Create a new vehicle"""
    if request.method == 'POST':
        try:
            # Get form data
            registration_number = request.form.get('registration_number')
            vehicle_type = request.form.get('vehicle_type')
            model = request.form.get('model')
            if model == 'Other':
                model = request.form.get('custom_model', 'Other')
            year = request.form.get('year')
            capacity = request.form.get('capacity')
            daily_rate = request.form.get('daily_rate')
            
            # Enhanced fields
            hourly_rate = request.form.get('hourly_rate')
            per_km_rate = request.form.get('per_km_rate')
            has_ac = request.form.get('has_ac') == 'true'
            fuel_type = request.form.get('fuel_type')
            transmission = request.form.get('transmission')
            minimum_rental_hours = request.form.get('minimum_rental_hours', 4)
            night_charge_multiplier = request.form.get('night_charge_multiplier', 1.25)
            
            status = request.form.get('status', 'available')
            location = request.form.get('location')
            mileage = request.form.get('mileage', 0)
            
            # Log vehicle creation attempt
            logger.info(f"Creating new vehicle: {registration_number}, {model}, {year}")

            # Create new vehicle with enhanced fields
            vehicle = Vehicle(
                registration_number=registration_number,
                vehicle_type=vehicle_type,
                model=model,
                year=int(year),
                capacity=float(capacity),
                daily_rate=float(daily_rate),
                hourly_rate=float(hourly_rate),
                per_km_rate=float(per_km_rate),
                has_ac=has_ac,
                fuel_type=fuel_type,
                transmission=transmission,
                minimum_rental_hours=int(minimum_rental_hours),
                night_charge_multiplier=float(night_charge_multiplier),
                status=status,
                location=location,
                mileage=int(mileage)
            )

            # Save to database
            db.session.add(vehicle)
            db.session.commit()
            logger.info(f"Vehicle created successfully: ID {vehicle.id}")
            flash('Vehicle added successfully!', 'success')
            return redirect(url_for('vehicle.list_vehicles'))
        except ValueError as e:
            # Handle validation errors
            log_exception(e, "Validation error creating vehicle")
            flash(f'Invalid data: {str(e)}', 'danger')
            return render_template('vehicles/create.html', current_year=datetime.now().year)
        except Exception as e:
            # Handle other errors
            log_exception(e, "Unexpected error creating vehicle")
            db.session.rollback()
            flash('An error occurred while creating the vehicle', 'danger')
            return render_template('vehicles/create.html', current_year=datetime.now().year)

    return render_template('vehicles/create.html', current_year=datetime.now().year)

@vehicle_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_vehicle(id):
    """Update vehicle details"""
    try:
        vehicle = Vehicle.query.get_or_404(id)
        
        if request.method == 'POST':
            try:
                # Log update attempt
                logger.info(f"Updating vehicle ID {id}")
                
                # Update vehicle details
                vehicle.registration_number = request.form.get('registration_number')
                vehicle.vehicle_type = request.form.get('vehicle_type')
                model = request.form.get('model')
                if model == 'Other':
                    model = request.form.get('custom_model', 'Other')
                vehicle.model = model
                vehicle.year = int(request.form.get('year'))
                vehicle.capacity = float(request.form.get('capacity'))
                vehicle.daily_rate = float(request.form.get('daily_rate'))
                
                # Enhanced fields
                vehicle.hourly_rate = float(request.form.get('hourly_rate'))
                vehicle.per_km_rate = float(request.form.get('per_km_rate'))
                vehicle.has_ac = request.form.get('has_ac') == 'true'
                vehicle.fuel_type = request.form.get('fuel_type')
                vehicle.transmission = request.form.get('transmission')
                vehicle.minimum_rental_hours = int(request.form.get('minimum_rental_hours', 4))
                vehicle.night_charge_multiplier = float(request.form.get('night_charge_multiplier', 1.25))
                
                vehicle.status = request.form.get('status')
                vehicle.location = request.form.get('location')
                vehicle.mileage = int(request.form.get('mileage'))
                vehicle.updated_at = datetime.utcnow()
                
                # Save changes
                db.session.commit()
                logger.info(f"Vehicle ID {id} updated successfully")
                flash('Vehicle updated successfully!', 'success')
                return redirect(url_for('vehicle.view_vehicle', id=vehicle.id))
                
            except ValueError as e:
                # Handle validation errors
                log_exception(e, f"Validation error updating vehicle {id}")
                flash(f'Invalid data: {str(e)}', 'danger')
            except Exception as e:
                # Handle other errors
                log_exception(e, f"Unexpected error updating vehicle {id}")
                db.session.rollback()
                flash('An error occurred while updating the vehicle', 'danger')
        
        return render_template('vehicles/update.html', vehicle=vehicle, current_year=datetime.now().year)
        
    except Exception as e:
        log_exception(e, f"Error retrieving vehicle with ID {id} for update")
        flash('Vehicle not found or an error occurred', 'danger')
        return redirect(url_for('vehicle.list_vehicles'))

@vehicle_bp.route('/<int:id>/delete', methods=['POST'])
def delete_vehicle(id):
    """Delete a vehicle"""
    try:
        vehicle = Vehicle.query.get_or_404(id)
        
        # Log delete attempt
        logger.info(f"Deleting vehicle ID {id}: {vehicle.registration_number}")
        
        db.session.delete(vehicle)
        db.session.commit()
        
        logger.info(f"Vehicle ID {id} deleted successfully")
        flash('Vehicle deleted successfully!', 'success')
        
    except Exception as e:
        log_exception(e, f"Error deleting vehicle with ID {id}")
        db.session.rollback()
        flash('An error occurred while deleting the vehicle', 'danger')
        
    return redirect(url_for('vehicle.list_vehicles'))
