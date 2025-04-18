gym-management-system/
├── app.py                           # Main application file with database connection
├── README.md                        # Project documentation
├── routes/                          # Directory for route handlers
│   ├── __init__.py                  # Empty file to mark directory as a Python package
│   ├── customer_routes.py           # Routes for customer management
│   ├── employee_routes.py           # Routes for employee management
│   ├── gym_routes.py                # Routes for gym management
│   ├── class_routes.py              # Routes for class management
│   ├── supplement_routes.py         # Routes for supplement management
│   ├── membership_routes.py         # Routes for membership management
│   └── billing_routes.py            # Routes for billing management
├── templates/                       # Directory for HTML templates
│   ├── base.html                    # Base template with common layout
│   ├── index.html                   # Home page template
│   ├── customers/                   # Templates for customer management
│   │   ├── index.html               # List of customers
│   │   ├── add.html                 # Add customer form
│   │   ├── view.html                # View customer details
│   │   ├── edit.html                # Edit customer form
│   │   └── emergency_contacts/      # Templates for emergency contacts
│   │       └── add.html             # Add emergency contact form
│   ├── employees/                   # Templates for employee management
│   │   ├── index.html               # List of employees
│   │   ├── add.html                 # Add employee form
│   │   ├── view.html                # View employee details
│   │   ├── edit.html                # Edit employee form
│   │   ├── certifications/          # Templates for certifications
│   │   │   └── add.html             # Add certification form
│   │   └── salaries/                # Templates for salaries
│   │       └── add.html             # Add salary form
│   ├── gyms/                        # Templates for gym management
│   │   ├── index.html               # List of gyms
│   │   ├── add.html                 # Add gym form
│   │   ├── view.html                # View gym details
│   │   ├── edit.html                # Edit gym form
│   │   └── locations/               # Templates for locations
│   │       └── add.html             # Add location form
│   ├── classes/                     # Templates for class management
│   │   ├── index.html               # List of classes
│   │   ├── add.html                 # Add class form
│   │   ├── view.html                # View class details
│   │   ├── edit.html                # Edit class form
│   │   ├── sessions/                # Templates for sessions
│   │   │   └── add.html             # Add session form
│   │   ├── prerequisites/           # Templates for prerequisites
│   │   │   └── add.html             # Add prerequisite form
│   │   └── equipment/               # Templates for equipment requirements
│   │       └── add.html             # Add equipment requirement form
│   ├── supplements/                 # Templates for supplement management
│   │   ├── index.html               # List of supplements
│   │   ├── add.html                 # Add supplement form
│   │   ├── view.html                # View supplement details
│   │   ├── edit.html                # Edit supplement form
│   │   ├── stocks/                  # Templates for stocks
│   │   │   └── add.html             # Add stock form
│   │   └── customer_usages/         # Templates for customer usages
│   │       └── add.html             # Add customer usage form
│   ├── memberships/                 # Templates for membership management
│   │   ├── index.html               # List of memberships
│   │   ├── add.html                 # Add membership form
│   │   ├── view.html                # View membership details
│   │   ├── edit.html                # Edit membership form
│   │   ├── transactions/            # Templates for transactions
│   │   │   └── add.html             # Add transaction form
│   │   └── plans/                   # Templates for subscription plans
│   │       ├── index.html           # List of subscription plans
│   │       ├── add.html             # Add subscription plan form
│   │       └── edit.html            # Edit subscription plan form
│   └── billings/                    # Templates for billing management
│       ├── index.html               # List of billings
│       ├── add.html                 # Add billing form
│       ├── view.html                # View billing details
│       ├── edit.html                # Edit billing form
│       ├── generate_invoice.html    # Generate invoice form
│       ├── invoice.html             # Invoice template
│       └── payment_methods/         # Templates for payment methods
│           └── add.html             # Add payment method form
└── static/                          # Directory for static files
    ├── css/                         # CSS files
    │   └── style.css                # Custom styles
    ├── js/                          # JavaScript files
    │   └── script.js                # Custom scripts
    └── img/                         # Image files
        └── logo.png                 # Application logo#   g y m _ m a n a g e m e n t _ v 0  
 