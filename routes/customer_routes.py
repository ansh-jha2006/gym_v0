from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Customer, EmergencyContact, CustomerFeedback, CustomerLog, CustomerSupport
from datetime import datetime

# Customer routes
@app.route('/customers')
def customers():
    customers = Customer.query.all()
    return render_template('customers/index.html', customers=customers)

@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d') if request.form['birthdate'] else None
        address = request.form['address']
        phone_number = request.form['phone_number']
        
        new_customer = Customer(
            FirstName=first_name,
            LastName=last_name,
            Birthdate=birthdate,
            Address=address,
            PhoneNumber=phone_number
        )
        
        try:
            db.session.add(new_customer)
            db.session.commit()
            flash('Customer added successfully!', 'success')
            return redirect(url_for('customers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding customer: {str(e)}', 'danger')
    
    return render_template('customers/add.html')

@app.route('/customers/<int:id>')
def view_customer(id):
    customer = Customer.query.get_or_404(id)
    emergency_contacts = EmergencyContact.query.filter_by(CustomerID=id).all()
    feedbacks = CustomerFeedback.query.filter_by(CustomerID=id).all()
    support_tickets = CustomerSupport.query.filter_by(CustomerID=id).all()
    
    return render_template(
        'customers/view.html', 
        customer=customer, 
        emergency_contacts=emergency_contacts,
        feedbacks=feedbacks,
        support_tickets=support_tickets
    )

@app.route('/customers/<int:id>/edit', methods=['GET', 'POST'])
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        customer.FirstName = request.form['first_name']
        customer.LastName = request.form['last_name']
        customer.Birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d') if request.form['birthdate'] else None
        customer.Address = request.form['address']
        customer.PhoneNumber = request.form['phone_number']
        
        try:
            db.session.commit()
            flash('Customer updated successfully!', 'success')
            return redirect(url_for('view_customer', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating customer: {str(e)}', 'danger')
    
    return render_template('customers/edit.html', customer=customer)

@app.route('/customers/<int:id>/delete', methods=['POST'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    
    try:
        db.session.delete(customer)
        db.session.commit()
        flash('Customer deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting customer: {str(e)}', 'danger')
    
    return redirect(url_for('customers'))

# Emergency Contact routes
@app.route('/customers/<int:customer_id>/emergency-contacts/add', methods=['GET', 'POST'])
def add_emergency_contact(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    if request.method == 'POST':
        contact_name = request.form['contact_name']
        relationship = request.form['relationship']
        phone_number = request.form['phone_number']
        
        new_contact = EmergencyContact(
            CustomerID=customer_id,
            ContactName=contact_name,
            Relationship=relationship,
            PhoneNumber=phone_number
        )
        
        try:
            db.session.add(new_contact)
            db.session.commit()
            flash('Emergency contact added successfully!', 'success')
            return redirect(url_for('view_customer', id=customer_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding emergency contact: {str(e)}', 'danger')
    
    return render_template('customers/emergency_contacts/add.html', customer=customer)

@app.route('/emergency-contacts/<int:id>/delete', methods=['POST'])
def delete_emergency_contact(id):
    contact = EmergencyContact.query.get_or_404(id)
    customer_id = contact.CustomerID
    
    try:
        db.session.delete(contact)
        db.session.commit()
        flash('Emergency contact deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting emergency contact: {str(e)}', 'danger')
    
    return redirect(url_for('view_customer', id=customer_id))