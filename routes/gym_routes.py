from flask import render_template, request, redirect, url_for, flash
from app import app, execute_query
from datetime import datetime

# Gym routes
@app.route('/gyms')
def gyms():
    query = "SELECT * FROM gym"
    gyms = execute_query(query, fetch=True)
    return render_template('gyms/index.html', gyms=gyms)

@app.route('/gyms/add', methods=['GET', 'POST'])
def add_gym():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone_number = request.form['phone_number']
        
        query = """
        INSERT INTO gym (Name, Address, CustomerPhoneNumber)
        VALUES (%s, %s, %s)
        """
        params = (name, address, phone_number)
        
        gym_id = execute_query(query, params)
        
        if gym_id:
            flash('Gym added successfully!', 'success')
            return redirect(url_for('gyms'))
        else:
            flash('Error adding gym', 'danger')
    
    return render_template('gyms/add.html')

@app.route('/gyms/<int:id>')
def view_gym(id):
    # Get gym details
    gym_query = "SELECT * FROM gym WHERE GymID = %s"
    gyms = execute_query(gym_query, (id,), fetch=True)
    
    if not gyms:
        flash('Gym not found', 'danger')
        return redirect(url_for('gyms'))
    
    gym = gyms[0]
    
    # Get locations
    location_query = "SELECT * FROM location WHERE GymID = %s"
    locations = execute_query(location_query, (id,), fetch=True)
    
    # Get employees
    employee_query = "SELECT * FROM gymemployee WHERE GymID = %s"
    employees = execute_query(employee_query, (id,), fetch=True)
    
    # Get workout classes
    class_query = """
    SELECT wc.* 
    FROM workoutclass wc
    JOIN gymhostsworkoutclass ghwc ON wc.WorkoutClassID = ghwc.WorkoutClassID
    WHERE ghwc.GymID = %s
    """
    classes = execute_query(class_query, (id,), fetch=True)
    
    return render_template(
        'gyms/view.html', 
        gym=gym, 
        locations=locations,
        employees=employees,
        classes=classes
    )

@app.route('/gyms/<int:id>/edit', methods=['GET', 'POST'])
def edit_gym(id):
    # Get gym details
    gym_query = "SELECT * FROM gym WHERE GymID = %s"
    gyms = execute_query(gym_query, (id,), fetch=True)
    
    if not gyms:
        flash('Gym not found', 'danger')
        return redirect(url_for('gyms'))
    
    gym = gyms[0]
    
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone_number = request.form['phone_number']
        
        query = """
        UPDATE gym 
        SET Name = %s, Address = %s, CustomerPhoneNumber = %s
        WHERE GymID = %s
        """
        params = (name, address, phone_number, id)
        
        result = execute_query(query, params)
        
        if result is not None:
            flash('Gym updated successfully!', 'success')
            return redirect(url_for('view_gym', id=id))
        else:
            flash('Error updating gym', 'danger')
    
    return render_template('gyms/edit.html', gym=gym)

@app.route('/gyms/<int:id>/delete', methods=['POST'])
def delete_gym(id):
    query = "DELETE FROM gym WHERE GymID = %s"
    result = execute_query(query, (id,))
    
    if result is not None:
        flash('Gym deleted successfully!', 'success')
    else:
        flash('Error deleting gym', 'danger')
    
    return redirect(url_for('gyms'))

# Location routes
@app.route('/gyms/<int:gym_id>/locations/add', methods=['GET', 'POST'])
def add_location(gym_id):
    # Check if gym exists
    gym_query = "SELECT * FROM gym WHERE GymID = %s"
    gyms = execute_query(gym_query, (gym_id,), fetch=True)
    
    if not gyms:
        flash('Gym not found', 'danger')
        return redirect(url_for('gyms'))
    
    gym = gyms[0]
    
    if request.method == 'POST':
        floor_number = request.form['floor_number']
        room_name = request.form['room_name']
        description = request.form['description']
        
        query = """
        INSERT INTO location (GymID, FloorNumber, RoomName, Description)
        VALUES (%s, %s, %s, %s)
        """
        params = (gym_id, floor_number, room_name, description)
        
        location_id = execute_query(query, params)
        
        if location_id:
            flash('Location added successfully!', 'success')
            return redirect(url_for('view_gym', id=gym_id))
        else:
            flash('Error adding location', 'danger')
    
    return render_template('gyms/locations/add.html', gym=gym)

@app.route('/locations/<int:id>/delete', methods=['POST'])
def delete_location(id):
    # Get gym ID first for redirect
    query = "SELECT GymID FROM location WHERE LocationID = %s"
    results = execute_query(query, (id,), fetch=True)
    
    if not results:
        flash('Location not found', 'danger')
        return redirect(url_for('gyms'))
    
    gym_id = results[0]['GymID']
    
    # Delete the location
    delete_query = "DELETE FROM location WHERE LocationID = %s"
    result = execute_query(delete_query, (id,))
    
    if result is not None:
        flash('Location deleted successfully!', 'success')
    else:
        flash('Error deleting location', 'danger')
    
    return redirect(url_for('view_gym', id=gym_id))