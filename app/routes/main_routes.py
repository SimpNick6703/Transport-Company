from flask import render_template, request, redirect, url_for, flash
from app.routes import main_bp
from app import db
from app.models import Vehicle, Customer, Rental
from datetime import datetime, timedelta
import json
import calendar

@main_bp.route('/')
@main_bp.route('/home')
def home():
    """Home page route"""
    # Get summary stats for dashboard
    total_vehicles = Vehicle.query.count()
    available_vehicles = Vehicle.query.filter_by(status='available').count()
    total_customers = Customer.query.count()
    active_rentals = Rental.query.filter_by(rental_status='active').count()
    
    return render_template('home.html', 
                          total_vehicles=total_vehicles,
                          available_vehicles=available_vehicles,
                          total_customers=total_customers,
                          active_rentals=active_rentals)

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard route with stats and overview"""
    
    # Calculate total revenue from completed rentals
    completed_rentals = Rental.query.filter_by(rental_status='completed').all()
    total_revenue = sum(rental.total_amount or 0 for rental in completed_rentals)
    
    # Calculate fleet utilization rate
    total_vehicles = Vehicle.query.count()
    rented_vehicles = Vehicle.query.filter_by(status='rented').count()
    utilization_rate = round((rented_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0, 1)
    
    # Get upcoming returns (next 48 hours)
    now = datetime.utcnow()
    end_date_cutoff = now + timedelta(days=2)
    upcoming_rental_returns = Rental.query.filter(
        Rental.rental_status == 'active',
        Rental.end_date <= end_date_cutoff,
        Rental.end_date >= now
    ).order_by(Rental.end_date).all()
    upcoming_returns = len(upcoming_rental_returns)
    
    # Get vehicles due for maintenance
    maintenance_count = Vehicle.query.filter_by(status='maintenance').count()
    
    # Get recent rental activity
    recent_rentals = Rental.query.order_by(Rental.created_at.desc()).limit(5).all()
    
    # Generate monthly revenue data for chart (last 6 months)
    months = []
    monthly_revenue = []
    
    # Get current month and previous 5 months
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    
    for i in range(5, -1, -1):
        # Calculate month and year
        month_num = (current_month - i) % 12
        if month_num == 0:
            month_num = 12
        year = current_year - ((current_month - month_num) // 12)
        
        # First day of the month
        first_day = datetime(year, month_num, 1)
        
        # Last day of the month
        if month_num == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(year, month_num + 1, 1) - timedelta(days=1)
        
        # Get completed rentals for this month
        month_rentals = Rental.query.filter(
            Rental.rental_status == 'completed',
            Rental.return_date >= first_day,
            Rental.return_date <= last_day
        ).all()
        
        # Calculate total revenue for the month
        month_revenue = sum(rental.total_amount or 0 for rental in month_rentals)
        
        # Add to data arrays
        months.append(f"'{calendar.month_name[month_num][:3]} {str(year)[-2:]}'")
        monthly_revenue.append(month_revenue)
    
    # Get vehicle types distribution for pie chart
    vehicle_types = []
    vehicle_type_counts = []
    
    # Get distinct vehicle types
    vehicle_type_results = db.session.query(Vehicle.vehicle_type, db.func.count(Vehicle.id)).group_by(Vehicle.vehicle_type).all()
    
    for v_type, count in vehicle_type_results:
        vehicle_types.append(f"'{v_type}'")
        vehicle_type_counts.append(count)
    
    return render_template('dashboard.html',
                           total_revenue="{:.2f}".format(total_revenue),
                           utilization_rate=utilization_rate,
                           upcoming_returns=upcoming_returns,
                           maintenance_count=maintenance_count,
                           recent_rentals=recent_rentals,
                           upcoming_rental_returns=upcoming_rental_returns,
                           months=f"[{', '.join(months)}]",
                           monthly_revenue=monthly_revenue,
                           vehicle_types=f"[{', '.join(vehicle_types)}]",
                           vehicle_type_counts=vehicle_type_counts)