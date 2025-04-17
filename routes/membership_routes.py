from flask import render_template, request, redirect, url_for, flash
from app import app, execute_query
from datetime import datetime

# Membership routes
@app.route('/memberships')
def memberships():
    query = """
    SELECT gm.*, c.FirstName, c.LastName 
    FROM gymmembership gm
    LEFT JOIN customer c ON gm.CustomerID = c.CustomerID
    """
    memberships = execute_query(query, fetch=True)
    return render_template('memberships/index.html', memberships=memberships)

@app.route('/memberships/add', methods=['GET', 'POST'])
def add_membership():
    # Get all customers for the dropdown
    customers_query = "SELECT * FROM customer"
    customers = execute_query(customers_query, fetch=True)
    
    # Get all subscription plans for the dropdown
    plans_query = "SELECT * FROM subscription_plan"
    plans = execute_query(plans_query, fetch=True)
    
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        
        query = """
        INSERT INTO gymmembership (CustomerID)
        VALUES (%s)
        """
        params = (customer_id,)
        
        membership_id = execute_query(query, params)
        
        if membership_id:
            # Add entry to customermembership junction table
            junction_query = """
            INSERT INTO customermembership (CustomerID, GymMembershipID)
            VALUES (%s, %s)
            """
            junction_params = (customer_id, membership_id)
            execute_query(junction_query, junction_params)
            
            flash('Membership added successfully!', 'success')
            return redirect(url_for('memberships'))
        else:
            flash('Error adding membership', 'danger')
    
    return render_template('memberships/add.html', customers=customers, plans=plans)

@app.route('/memberships/<int:id>')
def view_membership(id):
    # Get membership details
    membership_query = """
    SELECT gm.*, c.FirstName, c.LastName 
    FROM gymmembership gm
    LEFT JOIN customer c ON gm.CustomerID = c.CustomerID
    WHERE gm.GymMembershipID = %s
    """
    memberships = execute_query(membership_query, (id,), fetch=True)
    
    if not memberships:
        flash('Membership not found', 'danger')
        return redirect(url_for('memberships'))
    
    membership = memberships[0]
    
    # Get transactions
    transaction_query = "SELECT * FROM membership_transaction_log WHERE GymMembershipID = %s"
    transactions = execute_query(transaction_query, (id,), fetch=True)
    
    return render_template(
        'memberships/view.html', 
        membership=membership, 
        transactions=transactions
    )

@app.route('/memberships/<int:id>/edit', methods=['GET', 'POST'])
def edit_membership(id):
    # Get membership details
    membership_query = "SELECT * FROM gymmembership WHERE GymMembershipID = %s"
    memberships = execute_query(membership_query, (id,), fetch=True)
    
    if not memberships:
        flash('Membership not found', 'danger')
        return redirect(url_for('memberships'))
    
    membership = memberships[0]
    
    # Get all customers for the dropdown
    customers_query = "SELECT * FROM customer"
    customers = execute_query(customers_query, fetch=True)
    
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        
        query = """
        UPDATE gymmembership 
        SET CustomerID = %s
        WHERE GymMembershipID = %s
        """
        params = (customer_id, id)
        
        result = execute_query(query, params)
        
        if result is not None:
            # Update junction table
            junction_query = """
            UPDATE customermembership 
            SET CustomerID = %s
            WHERE GymMembershipID = %s
            """
            junction_params = (customer_id, id)
            execute_query(junction_query, junction_params)
            
            flash('Membership updated successfully!', 'success')
            return redirect(url_for('view_membership', id=id))
        else:
            flash('Error updating membership', 'danger')
    
    return render_template('memberships/edit.html', membership=membership, customers=customers)

@app.route('/memberships/<int:id>/delete', methods=['POST'])
def delete_membership(id):
    # Delete from junction table first
    junction_query = "DELETE FROM customermembership WHERE GymMembershipID = %s"
    execute_query(junction_query, (id,))
    
    # Delete the membership
    query = "DELETE FROM gymmembership WHERE GymMembershipID = %s"
    result = execute_query(query, (id,))
    
    if result is not None:
        flash('Membership deleted successfully!', 'success')
    else:
        flash('Error deleting membership', 'danger')
    
    return redirect(url_for('memberships'))

# Transaction routes
@app.route('/memberships/<int:membership_id>/transactions/add', methods=['GET', 'POST'])
def add_transaction(membership_id):
    # Check if membership exists
    membership_query = """
    SELECT gm.*, c.FirstName, c.LastName 
    FROM gymmembership gm
    LEFT JOIN customer c ON gm.CustomerID = c.CustomerID
    WHERE gm.GymMembershipID = %s
    """
    memberships = execute_query(membership_query, (membership_id,), fetch=True)
    
    if not memberships:
        flash('Membership not found', 'danger')
        return redirect(url_for('memberships'))
    
    membership = memberships[0]
    
    if request.method == 'POST':
        transaction_date = request.form['transaction_date']
        status = request.form['status']
        amount_paid = request.form['amount_paid']
        
        query = """
        INSERT INTO membership_transaction_log (CustomerID, GymMembershipID, TransactionDate, Status, AmountPaid)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (membership['CustomerID'], membership_id, transaction_date, status, amount_paid)
        
        transaction_id = execute_query(query, params)
        
        if transaction_id:
            flash('Transaction added successfully!', 'success')
            return redirect(url_for('view_membership', id=membership_id))
        else:
            flash('Error adding transaction', 'danger')
    
    return render_template('memberships/transactions/add.html', membership=membership)

@app.route('/transactions/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    # Get membership ID first for redirect
    query = "SELECT GymMembershipID FROM membership_transaction_log WHERE TransactionID = %s"
    results = execute_query(query, (id,), fetch=True)
    
    if not results:
        flash('Transaction not found', 'danger')
        return redirect(url_for('memberships'))
    
    membership_id = results[0]['GymMembershipID']
    
    # Delete the transaction
    delete_query = "DELETE FROM membership_transaction_log WHERE TransactionID = %s"
    result = execute_query(delete_query, (id,))
    
    if result is not None:
        flash('Transaction deleted successfully!', 'success')
    else:
        flash('Error deleting transaction', 'danger')
    
    return redirect(url_for('view_membership', id=membership_id))

# Subscription Plan routes
@app.route('/subscription-plans')
def subscription_plans():
    query = "SELECT * FROM subscription_plan"
    plans = execute_query(query, fetch=True)
    return render_template('memberships/plans/index.html', plans=plans)

@app.route('/subscription-plans/add', methods=['GET', 'POST'])
def add_subscription_plan():
    if request.method == 'POST':
        plan_name = request.form['plan_name']
        duration_months = request.form['duration_months']
        price = request.form['price']
        
        query = """
        INSERT INTO subscription_plan (PlanName, DurationMonths, Price)
        VALUES (%s, %s, %s)
        """
        params = (plan_name, duration_months, price)
        
        plan_id = execute_query(query, params)
        
        if plan_id:
            flash('Subscription plan added successfully!', 'success')
            return redirect(url_for('subscription_plans'))
        else:
            flash('Error adding subscription plan', 'danger')
    
    return render_template('memberships/plans/add.html')

@app.route('/subscription-plans/<int:id>/edit', methods=['GET', 'POST'])
def edit_subscription_plan(id):
    # Get plan details
    plan_query = "SELECT * FROM subscription_plan WHERE PlanID = %s"
    plans = execute_query(plan_query, (id,), fetch=True)
    
    if not plans:
        flash('Subscription plan not found', 'danger')
        return redirect(url_for('subscription_plans'))
    
    plan = plans[0]
    
    if request.method == 'POST':
        plan_name = request.form['plan_name']
        duration_months = request.form['duration_months']
        price = request.form['price']
        
        query = """
        UPDATE subscription_plan 
        SET PlanName = %s, DurationMonths = %s, Price = %s
        WHERE PlanID = %s
        """
        params = (plan_name, duration_months, price, id)
        
        result = execute_query(query, params)
        
        if result is not None:
            flash('Subscription plan updated successfully!', 'success')
            return redirect(url_for('subscription_plans'))
        else:
            flash('Error updating subscription plan', 'danger')
    
    return render_template('memberships/plans/edit.html', plan=plan)

@app.route('/subscription-plans/<int:id>/delete', methods=['POST'])
def delete_subscription_plan(id):
    query = "DELETE FROM subscription_plan WHERE PlanID = %s"
    result = execute_query(query, (id,))
    
    if result is not None:
        flash('Subscription plan deleted successfully!', 'success')
    else:
        flash('Error deleting subscription plan', 'danger')
    
    return redirect(url_for('subscription_plans'))