from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Supplement, SupplementStock, SupplementUsageCustomer, SupplementUsageTrainer, Gym, Customer, GymEmployee
from datetime import datetime

# Supplement routes
@app.route('/supplements')
def supplements():
    supplements = Supplement.query.all()
    return render_template('supplements/index.html', supplements=supplements)

@app.route('/supplements/add', methods=['GET', 'POST'])
def add_supplement():
    if request.method == 'POST':
        name = request.form['name']
        brand = request.form['brand']
        type = request.form['type']
        description = request.form['description']
        
        new_supplement = Supplement(
            Name=name,
            Brand=brand,
            Type=type,
            Description=description
        )
        
        try:
            db.session.add(new_supplement)
            db.session.commit()
            flash('Supplement added successfully!', 'success')
            return redirect(url_for('supplements'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding supplement: {str(e)}', 'danger')
    
    return render_template('supplements/add.html')

@app.route('/supplements/<int:id>')
def view_supplement(id):
    supplement = Supplement.query.get_or_404(id)
    stocks = SupplementStock.query.filter_by(SupplementID=id).all()
    customer_usages = SupplementUsageCustomer.query.filter_by(SupplementID=id).all()
    trainer_usages = SupplementUsageTrainer.query.filter_by(SupplementID=id).all()
    
    return render_template(
        'supplements/view.html', 
        supplement=supplement, 
        stocks=stocks,
        customer_usages=customer_usages,
        trainer_usages=trainer_usages
    )

@app.route('/supplements/<int:id>/edit', methods=['GET', 'POST'])
def edit_supplement(id):
    supplement = Supplement.query.get_or_404(id)
    
    if request.method == 'POST':
        supplement.Name = request.form['name']
        supplement.Brand = request.form['brand']
        supplement.Type = request.form['type']
        supplement.Description = request.form['description']
        
        try:
            db.session.commit()
            flash('Supplement updated successfully!', 'success')
            return redirect(url_for('view_supplement', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating supplement: {str(e)}', 'danger')
    
    return render_template('supplements/edit.html', supplement=supplement)

@app.route('/supplements/<int:id>/delete', methods=['POST'])
def delete_supplement(id):
    supplement = Supplement.query.get_or_404(id)
    
    try:
        db.session.delete(supplement)
        db.session.commit()
        flash('Supplement deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting supplement: {str(e)}', 'danger')
    
    return redirect(url_for('supplements'))

# Supplement Stock routes
@app.route('/supplements/<int:supplement_id>/stocks/add', methods=['GET', 'POST'])
def add_supplement_stock(supplement_id):
    supplement = Supplement.query.get_or_404(supplement_id)
    gyms = Gym.query.all()
    
    if request.method == 'POST':
        gym_id = request.form['gym_id']
        quantity = request.form['quantity']
        last_restocked = datetime.strptime(request.form['last_restocked'], '%Y-%m-%d') if request.form['last_restocked'] else None
        expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d') if request.form['expiry_date'] else None
        
        new_stock = SupplementStock(
            SupplementID=supplement_id,
            GymID=gym_id,
            Quantity=quantity,
            LastRestocked=last_restocked,
            ExpiryDate=expiry_date
        )
        
        try:
            db.session.add(new_stock)
            db.session.commit()
            flash('Stock added successfully!', 'success')
            return redirect(url_for('view_supplement', id=supplement_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding stock: {str(e)}', 'danger')
    
    return render_template('supplements/stocks/add.html', supplement=supplement, gyms=gyms)

@app.route('/supplement-stocks/<int:id>/delete', methods=['POST'])
def delete_supplement_stock(id):
    stock = SupplementStock.query.get_or_404(id)
    supplement_id = stock.SupplementID
    
    try:
        db.session.delete(stock)
        db.session.commit()
        flash('Stock deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting stock: {str(e)}', 'danger')
    
    return redirect(url_for('view_supplement', id=supplement_id))

# Customer Usage routes
@app.route('/supplements/<int:supplement_id>/customer-usages/add', methods=['GET', 'POST'])
def add_customer_usage(supplement_id):
    supplement = Supplement.query.get_or_404(supplement_id)
    customers = Customer.query.all()
    
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d') if request.form['start_date'] else None
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d') if request.form['end_date'] else None
        dosage = request.form['dosage']
        
        new_usage = SupplementUsageCustomer(
            SupplementID=supplement_id,
            CustomerID=customer_id,
            StartDate=start_date,
            EndDate=end_date,
            Dosage=dosage
        )
        
        try:
            db.session.add(new_usage)
            db.session.commit()
            flash('Customer usage added successfully!', 'success')
            return redirect(url_for('view_supplement', id=supplement_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding customer usage: {str(e)}', 'danger')
    
    return render_template('supplements/customer_usages/add.html', supplement=supplement, customers=customers)

@app.route('/customer-usages/<int:id>/delete', methods=['POST'])
def delete_customer_usage(id):
    usage = SupplementUsageCustomer.query.get_or_404(id)
    supplement_id = usage.SupplementID
    
    try:
        db.session.delete(usage)
        db.session.commit()
        flash('Customer usage deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting customer usage: {str(e)}', 'danger')
    
    return redirect(url_for('view_supplement', id=supplement_id))