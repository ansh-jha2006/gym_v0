from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import GymEmployee, EmployeeAttendance, EmployeeCertification, GymManager, ManagerSchedule, Gym, Salary
from datetime import datetime

# Employee routes
@app.route('/employees')
def employees():
    employees = GymEmployee.query.all()
    return render_template('employees/index.html', employees=employees)

@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    gyms = Gym.query.all()
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gym_id = request.form['gym_id']
        
        new_employee = GymEmployee(
            FirstName=first_name,
            LastName=last_name,
            GymID=gym_id
        )
        
        try:
            db.session.add(new_employee)
            db.session.commit()
            flash('Employee added successfully!', 'success')
            return redirect(url_for('employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding employee: {str(e)}', 'danger')
    
    return render_template('employees/add.html', gyms=gyms)

@app.route('/employees/<int:id>')
def view_employee(id):
    employee = GymEmployee.query.get_or_404(id)
    certifications = EmployeeCertification.query.filter_by(EmployeeID=id).all()
    attendances = EmployeeAttendance.query.filter_by(EmployeeID=id).all()
    salaries = Salary.query.filter_by(EmployeeID=id).all()
    
    # Check if employee is a manager
    manager = GymManager.query.filter_by(EmployeeID=id).first()
    manager_schedules = None
    
    if manager:
        manager_schedules = ManagerSchedule.query.filter_by(ManagerID=manager.ManagerID).all()
    
    return render_template(
        'employees/view.html', 
        employee=employee, 
        certifications=certifications,
        attendances=attendances,
        salaries=salaries,
        manager=manager,
        manager_schedules=manager_schedules
    )

@app.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
def edit_employee(id):
    employee = GymEmployee.query.get_or_404(id)
    gyms = Gym.query.all()
    
    if request.method == 'POST':
        employee.FirstName = request.form['first_name']
        employee.LastName = request.form['last_name']
        employee.GymID = request.form['gym_id']
        
        try:
            db.session.commit()
            flash('Employee updated successfully!', 'success')
            return redirect(url_for('view_employee', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating employee: {str(e)}', 'danger')
    
    return render_template('employees/edit.html', employee=employee, gyms=gyms)

@app.route('/employees/<int:id>/delete', methods=['POST'])
def delete_employee(id):
    employee = GymEmployee.query.get_or_404(id)
    
    try:
        db.session.delete(employee)
        db.session.commit()
        flash('Employee deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting employee: {str(e)}', 'danger')
    
    return redirect(url_for('employees'))

# Employee Certification routes
@app.route('/employees/<int:employee_id>/certifications/add', methods=['GET', 'POST'])
def add_certification(employee_id):
    employee = GymEmployee.query.get_or_404(employee_id)
    
    if request.method == 'POST':
        certification_name = request.form['certification_name']
        issued_by = request.form['issued_by']
        issue_date = datetime.strptime(request.form['issue_date'], '%Y-%m-%d') if request.form['issue_date'] else None
        expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d') if request.form['expiry_date'] else None
        
        new_certification = EmployeeCertification(
            EmployeeID=employee_id,
            CertificationName=certification_name,
            IssuedBy=issued_by,
            IssueDate=issue_date,
            ExpiryDate=expiry_date
        )
        
        try:
            db.session.add(new_certification)
            db.session.commit()
            flash('Certification added successfully!', 'success')
            return redirect(url_for('view_employee', id=employee_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding certification: {str(e)}', 'danger')
    
    return render_template('employees/certifications/add.html', employee=employee)

@app.route('/certifications/<int:id>/delete', methods=['POST'])
def delete_certification(id):
    certification = EmployeeCertification.query.get_or_404(id)
    employee_id = certification.EmployeeID
    
    try:
        db.session.delete(certification)
        db.session.commit()
        flash('Certification deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting certification: {str(e)}', 'danger')
    
    return redirect(url_for('view_employee', id=employee_id))

# Salary routes
@app.route('/employees/<int:employee_id>/salaries/add', methods=['GET', 'POST'])
def add_salary(employee_id):
    employee = GymEmployee.query.get_or_404(employee_id)
    
    if request.method == 'POST':
        amount = request.form['amount']
        month = request.form['month']
        year = request.form['year']
        payment_date = datetime.strptime(request.form['payment_date'], '%Y-%m-%d') if request.form['payment_date'] else None
        
        new_salary = Salary(
            EmployeeID=employee  else None
        
        new_salary = Salary(
            EmployeeID=employee_id,
            Amount=amount,
            Month=month,
            Year=year,
            PaymentDate=payment_date
        )
        
        try:
            db.session.add(new_salary)
            db.session.commit()
            flash('Salary record added successfully!', 'success')
            return redirect(url_for('view_employee', id=employee_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding salary record: {str(e)}', 'danger')
    
    return render_template('employees/salaries/add.html', employee=employee)

@app.route('/salaries/<int:id>/delete', methods=['POST'])
def delete_salary(id):
    salary = Salary.query.get_or_404(id)
    employee_id = salary.EmployeeID
    
    try:
        db.session.delete(salary)
        db.session.commit()
        flash('Salary record deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting salary record: {str(e)}', 'danger')
    
    return redirect(url_for('view_employee', id=employee_id))