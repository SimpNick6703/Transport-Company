from flask import render_template, request, redirect, url_for, flash, jsonify
from app.routes import customer_bp
from app import db
from app.models import Customer
from datetime import datetime

@customer_bp.route('/')
def list_customers():
    """List all customers"""
    customers = Customer.query.all()
    return render_template('customers/index.html', customers=customers)

@customer_bp.route('/<int:id>')
def view_customer(id):
    """View customer details"""
    customer = Customer.query.get_or_404(id)
    return render_template('customers/view.html', customer=customer)

@customer_bp.route('/create', methods=['GET', 'POST'])
def create_customer():
    """Create a new customer"""
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        driving_license_number = request.form.get('driving_license_number')
        license_expiry_date = request.form.get('license_expiry_date')
        customer_type = request.form.get('customer_type', 'individual')

        # Create new customer
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            driving_license_number=driving_license_number,
            license_expiry_date=datetime.strptime(license_expiry_date, '%Y-%m-%d').date(),
            customer_type=customer_type
        )

        # Save to database
        db.session.add(customer)
        db.session.commit()
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customer.list_customers'))

    return render_template('customers/create.html')

@customer_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_customer(id):
    """Update customer details"""
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        # Update customer details
        customer.first_name = request.form.get('first_name')
        customer.last_name = request.form.get('last_name')
        customer.email = request.form.get('email')
        customer.phone = request.form.get('phone')
        customer.address = request.form.get('address')
        customer.driving_license_number = request.form.get('driving_license_number')
        customer.license_expiry_date = datetime.strptime(request.form.get('license_expiry_date'), '%Y-%m-%d').date()
        customer.customer_type = request.form.get('customer_type')
        customer.updated_at = datetime.utcnow()
        
        # Save changes
        db.session.commit()
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customer.view_customer', id=customer.id))
    
    return render_template('customers/update.html', customer=customer)

@customer_bp.route('/<int:id>/delete', methods=['POST'])
def delete_customer(id):
    """Delete a customer"""
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('customer.list_customers'))