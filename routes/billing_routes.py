from flask import render_template, request, redirect, url_for, flash
from app import app, execute_query
from datetime import datetime

# Billing routes
@app.route('/billings')
def billings():
    query = """
    SELECT b.*, c.FirstName, c.LastName 
    FROM billing b
    LEFT JOIN customer c ON b.CustomerID = c.CustomerID
    """
    billings = execute_query(query, fetch=True)
    return render_template('billings/index.html', billings=billings)

@app.route('/billings/add', methods=['GET', 'POST'])
def add_billing():
    # Get all customers for the dropdown
    customers_query = "SELECT * FROM customer"
    customers = execute_query(customers_query, fetch=True)
    
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        amount = request.form['amount']
        billing_date = request.form['billing_date']
        description = request.form['description']
        
        query = """
        INSERT INTO billing (CustomerID, Amount, BillingDate, Description)
        VALUES (%s, %s, %s, %s)
        """
        params = (customer_id, amount, billing_date, description)
        
        bill_id = execute_query(query, params)
        
        if bill_id:
            flash('Billing record added successfully!', 'success')
            return redirect(url_for('billings'))
        else:
            flash('Error adding billing record', 'danger')
    
    return render_template('billings/add.html', customers=customers)

@app.route('/billings/<int:id>')
def view_billing(id):
    # Get billing details
    billing_query = """
    SELECT b.*, c.FirstName, c.LastName 
    FROM billing b
    LEFT JOIN customer c ON b.CustomerID = c.CustomerID
    WHERE b.BillID = %s
    """
    billings = execute_query(billing_query, (id,), fetch=True)
    
    if not billings:
        flash('Billing record not found', 'danger')
        return redirect(url_for('billings'))
    
    billing = billings[0]
    
    # Get payment methods for this customer
    payment_query = "SELECT * FROM payment_method WHERE CustomerID = %s"
    payment_methods = execute_query(payment_query, (billing['CustomerID'],), fetch=True)
    
    return render_template('billings/view.html', billing=billing, payment_methods=payment_methods)

@app.route('/billings/<int:id>/edit', methods=['GET', 'POST'])
def edit_billing(id):
    # Get billing details
    billing_query = "SELECT * FROM billing WHERE BillID = %s"
    billings = execute_query(billing_query, (id,), fetch=True)
    
    if not billings:
        flash('Billing record not found', 'danger')
        return redirect(url_for('billings'))
    
    billing = billings[0]
    
    # Get all customers for the dropdown
    customers_query = "SELECT * FROM customer"
    customers = execute_query(customers_query, fetch=True)
    
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        amount = request.form['amount']
        billing_date = request.form['billing_date']
        description = request.form['description']
        
        query = """
        UPDATE billing 
        SET CustomerID = %s, Amount = %s, BillingDate = %s, Description = %s
        WHERE BillID = %s
        """
        params = (customer_id, amount, billing_date, description, id)
        
        result = execute_query(query, params)
        
        if result is not None:
            flash('Billing record updated successfully!', 'success')
            return redirect(url_for('view_billing', id=id))
        else:
            flash('Error updating billing record', 'danger')
    
    return render_template('billings/edit.html', billing=billing, customers=customers)

@app.route('/billings/<int:id>/delete', methods=['POST'])
def delete_billing(id):
    query = "DELETE FROM billing WHERE BillID = %s"
    result = execute_query(query, (id,))
    
    if result is not None:
        flash('Billing record deleted successfully!', 'success')
    else:
        flash('Error deleting billing record', 'danger')
    
    return redirect(url_for('billings'))

# Payment Method routes
@app.route('/customers/<int:customer_id>/payment-methods/add', methods=['GET', 'POST'])
def add_payment_method(customer_id):
    # Check if customer exists
    customer_query = "SELECT * FROM customer WHERE CustomerID = %s"
    customers = execute_query(customer_query, (customer_id,), fetch=True)
    
    if not customers:
        flash('Customer not found', 'danger')
        return redirect(url_for('customers'))
    
    customer = customers[0]
    
    if request.method == 'POST':
        card_number = request.form['card_number']
        expiry_date = request.form['expiry_date']
        card_type = request.form['card_type']
        
        query = """
        INSERT INTO payment_method (CustomerID, CardNumber, ExpiryDate, CardType)
        VALUES (%s, %s, %s, %s)
        """
        params = (customer_id, card_number, expiry_date, card_type)
        
        payment_id = execute_query(query, params)
        
        if payment_id:
            flash('Payment method added successfully!', 'success')
            return redirect(url_for('view_customer', id=customer_id))
        else:
            flash('Error adding payment method', 'danger')
    
    return render_template('billings/payment_methods/add.html', customer=customer)

@app.route('/payment-methods/<int:id>/delete', methods=['POST'])
def delete_payment_method(id):
    # Get customer ID first for redirect
    query = "SELECT CustomerID FROM payment_method WHERE PaymentMethodID = %s"
    results = execute_query(query, (id,), fetch=True)
    
    if not results:
        flash('Payment method not found', 'danger')
        return redirect(url_for('customers'))
    
    customer_id = results[0]['CustomerID']
    
    # Delete the payment method
    delete_query = "DELETE FROM payment_method WHERE PaymentMethodID = %s"
    result = execute_query(delete_query, (id,))
    
    if result is not None:
        flash('Payment method deleted successfully!', 'success')
    else:
        flash('Error deleting payment method', 'danger')
    
    return redirect(url_for('view_customer', id=customer_id))

# Generate Invoice
@app.route('/billings/generate-invoice', methods=['GET', 'POST'])
def generate_invoice():
    # Get all customers for the dropdown
    customers_query = "SELECT * FROM customer"
    customers = execute_query(customers_query, fetch=True)
    
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        # Get all billings for this customer in the date range
        query = """
        SELECT b.*, c.FirstName, c.LastName 
        FROM billing b
        LEFT JOIN customer c ON b.CustomerID = c.CustomerID
        WHERE b.CustomerID = %s AND b.BillingDate BETWEEN %s AND %s
        """
        params = (customer_id, start_date, end_date)
        
        billings = execute_query(query, params, fetch=True)
        
        # Get customer details
        customer_query = "SELECT * FROM customer WHERE CustomerID = %s"
        customers_result = execute_query(customer_query, (customer_id,), fetch=True)
        customer = customers_result[0] if customers_result else None
        
        return render_template(
            'billings/invoice.html', 
            billings=billings, 
            customer=customer,
            start_date=start_date,
            end_date=end_date
        )
    
    return render_template('billings/generate_invoice.html', customers=customers)