from flask import render_template, request, redirect, url_for, flash
from app import app, execute_query
from datetime import datetime

# Class routes
@app.route('/classes')
def classes():
    query = """
    SELECT wc.*, g.Name as GymName 
    FROM workoutclass wc
    LEFT JOIN gym g ON wc.GymID = g.GymID
    """
    classes = execute_query(query, fetch=True)
    return render_template('classes/index.html', classes=classes)

@app.route('/classes/add', methods=['GET', 'POST'])
def add_class():
    # Get all gyms for the dropdown
    gyms_query = "SELECT * FROM gym"
    gyms = execute_query(gyms_query, fetch=True)
    
    if request.method == 'POST':
        workout_class_name = request.form['workout_class_name']
        gym_id = request.form['gym_id']
        
        query = """
        INSERT INTO workoutclass (WorkoutClassName, GymID)
        VALUES (%s, %s)
        """
        params = (workout_class_name, gym_id)
        
        class_id = execute_query(query, params)
        
        if class_id:
            # Add entry to gymhostsworkoutclass junction table
            junction_query = """
            INSERT INTO gymhostsworkoutclass (GymID, WorkoutClassID)
            VALUES (%s, %s)
            """
            junction_params = (gym_id, class_id)
            execute_query(junction_query, junction_params)
            
            flash('Workout class added successfully!', 'success')
            return redirect(url_for('classes'))
        else:
            flash('Error adding workout class', 'danger')
    
    return render_template('classes/add.html', gyms=gyms)

@app.route('/classes/<int:id>')
def view_class(id):
    # Get class details
    class_query = """
    SELECT wc.*, g.Name as GymName 
    FROM workoutclass wc
    LEFT JOIN gym g ON wc.GymID = g.GymID
    WHERE wc.WorkoutClassID = %s
    """
    classes = execute_query(class_query, (id,), fetch=True)
    
    if not classes:
        flash('Workout class not found', 'danger')
        return redirect(url_for('classes'))
    
    workout_class = classes[0]
    
    # Get sessions
    session_query = """
    SELECT cs.*, e.FirstName, e.LastName 
    FROM class_session cs
    LEFT JOIN gymemployee e ON cs.EmployeeID = e.EmployeeID
    WHERE cs.WorkoutClassID = %s
    """
    sessions = execute_query(session_query, (id,), fetch=True)
    
    # Get prerequisites
    prereq_query = "SELECT * FROM class_prerequisite WHERE WorkoutClassID = %s"
    prerequisites = execute_query(prereq_query, (id,), fetch=True)
    
    # Get equipment requirements
    equip_query = """
    SELECT cer.*, g.Name as GymName 
    FROM class_equipment_requirement cer
    LEFT JOIN gym g ON cer.GymID = g.GymID
    WHERE cer.WorkoutClassID = %s
    """
    equipment_requirements = execute_query(equip_query, (id,), fetch=True)
    
    return render_template(
        'classes/view.html', 
        workout_class=workout_class, 
        sessions=sessions,
        prerequisites=prerequisites,
        equipment_requirements=equipment_requirements
    )

@app.route('/classes/<int:id>/edit', methods=['GET', 'POST'])
def edit_class(id):
    # Get class details
    class_query = "SELECT * FROM workoutclass WHERE WorkoutClassID = %s"
    classes = execute_query(class_query, (id,), fetch=True)
    
    if not classes:
        flash('Workout class not found', 'danger')
        return redirect(url_for('classes'))
    
    workout_class = classes[0]
    
    # Get all gyms for the dropdown
    gyms_query = "SELECT * FROM gym"
    gyms = execute_query(gyms_query, fetch=True)
    
    if request.method == 'POST':
        workout_class_name = request.form['workout_class_name']
        gym_id = request.form['gym_id']
        
        query = """
        UPDATE workoutclass 
        SET WorkoutClassName = %s, GymID = %s
        WHERE WorkoutClassID = %s
        """
        params = (workout_class_name, gym_id, id)
        
        result = execute_query(query, params)
        
        if result is not None:
            # Update junction table
            junction_query = """
            UPDATE gymhostsworkoutclass 
            SET GymID = %s
            WHERE WorkoutClassID = %s
            """
            junction_params = (gym_id, id)
            execute_query(junction_query, junction_params)
            
            flash('Workout class updated successfully!', 'success')
            return redirect(url_for('view_class', id=id))
        else:
            flash('Error updating workout class', 'danger')
    
    return render_template('classes/edit.html', workout_class=workout_class, gyms=gyms)

@app.route('/classes/<int:id>/delete', methods=['POST'])
def delete_class(id):
    # Delete from junction table first
    junction_query = "DELETE FROM gymhostsworkoutclass WHERE WorkoutClassID = %s"
    execute_query(junction_query, (id,))
    
    # Delete the class
    query = "DELETE FROM workoutclass WHERE WorkoutClassID = %s"
    result = execute_query(query, (id,))
    
    if result is not None:
        flash('Workout class deleted successfully!', 'success')
    else:
        flash('Error deleting workout class', 'danger')
    
    return redirect(url_for('classes'))

# Class Session routes
@app.route('/classes/<int:class_id>/sessions/add', methods=['GET', 'POST'])
def add_session(class_id):
    # Check if class exists
    class_query = "SELECT * FROM workoutclass WHERE WorkoutClassID = %s"
    classes = execute_query(class_query, (class_id,), fetch=True)
    
    if not classes:
        flash('Workout class not found', 'danger')
        return redirect(url_for('classes'))
    
    workout_class = classes[0]
    
    # Get all employees for the dropdown
    employees_query = "SELECT * FROM gymemployee"
    employees = execute_query(employees_query, fetch=True)
    
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        session_date = request.form['session_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        
        query = """
        INSERT INTO class_session (EmployeeID, WorkoutClassID, SessionDate, StartTime, EndTime)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (employee_id, class_id, session_date, start_time, end_time)
        
        session_id = execute_query(query, params)
        
        if session_id:
            flash('Session added successfully!', 'success')
            return redirect(url_for('view_class', id=class_id))
        else:
            flash('Error adding session', 'danger')
    
    return render_template('classes/sessions/add.html', workout_class=workout_class, employees=employees)

@app.route('/sessions/<int:id>/delete', methods=['POST'])
def delete_session(id):
    # Get class ID first for redirect
    query = "SELECT WorkoutClassID FROM class_session WHERE SessionID = %s"
    results = execute_query(query, (id,), fetch=True)
    
    if not results:
        flash('Session not found', 'danger')
        return redirect(url_for('classes'))
    
    class_id = results[0]['WorkoutClassID']
    
    # Delete the session
    delete_query = "DELETE FROM class_session WHERE SessionID = %s"
    result = execute_query(delete_query, (id,))
    
    if result is not None:
        flash('Session deleted successfully!', 'success')
    else:
        flash('Error deleting session', 'danger')
    
    return redirect(url_for('view_class', id=class_id))

# Class Prerequisite routes
@app.route('/classes/<int:class_id>/prerequisites/add', methods=['GET', 'POST'])
def add_prerequisite(class_id):
    # Check if class exists
    class_query = "SELECT * FROM workoutclass WHERE WorkoutClassID = %s"
    classes = execute_query(class_query, (class_id,), fetch=True)
    
    if not classes:
        flash('Workout class not found', 'danger')
        return redirect(url_for('classes'))
    
    workout_class = classes[0]
    
    if request.method == 'POST':
        requirement = request.form['requirement']
        
        query = """
        INSERT INTO class_prerequisite (WorkoutClassID, Requirement)
        VALUES (%s, %s)
        """
        params = (class_id, requirement)
        
        prereq_id = execute_query(query, params)
        
        if prereq_id:
            flash('Prerequisite added successfully!', 'success')
            return redirect(url_for('view_class', id=class_id))
        else:
            flash('Error adding prerequisite', 'danger')
    
    return render_template('classes/prerequisites/add.html', workout_class=workout_class)

@app.route('/prerequisites/<int:id>/delete', methods=['POST'])
def delete_prerequisite(id):
    # Get class ID first for redirect
    query = "SELECT WorkoutClassID FROM class_prerequisite WHERE PrerequisiteID = %s"
    results = execute_query(query, (id,), fetch=True)
    
    if not results:
        flash('Prerequisite not found', 'danger')
        return redirect(url_for('classes'))
    
    class_id = results[0]['WorkoutClassID']
    
    # Delete the prerequisite
    delete_query = "DELETE FROM class_prerequisite WHERE PrerequisiteID = %s"
    result = execute_query(delete_query, (id,))
    
    if result is not None:
        flash('Prerequisite deleted successfully!', 'success')
    else:
        flash('Error deleting prerequisite', 'danger')
    
    return redirect(url_for('view_class', id=class_id))

# Equipment Requirement routes
@app.route('/classes/<int:class_id>/equipment/add', methods=['GET', 'POST'])
def add_equipment_requirement(class_id):
    # Check if class exists
    class_query = "SELECT * FROM workoutclass WHERE WorkoutClassID = %s"
    classes = execute_query(class_query, (class_id,), fetch=True)
    
    if not classes:
        flash('Workout class not found', 'danger')
        return redirect(url_for('classes'))
    
    workout_class = classes[0]
    
    # Get all gyms for the dropdown
    gyms_query = "SELECT * FROM gym"
    gyms = execute_query(gyms_query, fetch=True)
    
    if request.method == 'POST':
        gym_id = request.form['gym_id']
        equipment_name = request.form['equipment_name']
        quantity = request.form['quantity']
        
        query = """
        INSERT INTO class_equipment_requirement (GymID, WorkoutClassID, EquipmentName, Quantity)
        VALUES (%s, %s, %s, %s)
        """
        params = (gym_id, class_id, equipment_name, quantity)
        
        equip_id = execute_query(query, params)
        
        if equip_id:
            flash('Equipment requirement added successfully!', 'success')
            return redirect(url_for('view_class', id=class_id))
        else:
            flash('Error adding equipment requirement', 'danger')
    
    return render_template('classes/equipment/add.html', workout_class=workout_class, gyms=gyms)

@app.route('/equipment/<int:id>/delete', methods=['POST'])
def delete_equipment_requirement(id):
    # Get class ID first for redirect
    query = "SELECT WorkoutClassID FROM class_equipment_requirement WHERE RequirementID = %s"
    results = execute_query(query, (id,), fetch=True)
    
    if not results:
        flash('Equipment requirement not found', 'danger')
        return redirect(url_for('classes'))
    
    class_id = results[0]['WorkoutClassID']
    
    # Delete the equipment requirement
    delete_query = "DELETE FROM class_equipment_requirement WHERE RequirementID = %s"
    result = execute_query(delete_query, (id,))
    
    if result is not None:
        flash('Equipment requirement deleted successfully!', 'success')
    else:
        flash('Error deleting equipment requirement', 'danger')
    
    return redirect(url_for('view_class', id=class_id))