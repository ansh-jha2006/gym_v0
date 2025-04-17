from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Ansh4306'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/gym_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models after db initialization to avoid circular imports
from models import *

# Routes for Home
@app.route('/')
def index():
    return render_template('index.html')

# Include routes for each section
from routes.customer_routes import *
from routes.employee_routes import *
from routes.gym_routes import *
from routes.class_routes import *
from routes.supplement_routes import *
from routes.membership_routes import *
from routes.billing_routes import *

if __name__ == '__main__':
    app.run(debug=True)