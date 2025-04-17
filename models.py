from app import db
from datetime import datetime

# Customer related models
class Customer(db.Model):
    __tablename__ = 'customer'
    CustomerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    Birthdate = db.Column(db.Date)
    Address = db.Column(db.String(255))
    PhoneNumber = db.Column(db.String(15))
    
    # Relationships
    emergency_contacts = db.relationship('EmergencyContact', backref='customer', lazy=True)
    feedbacks = db.relationship('CustomerFeedback', backref='customer', lazy=True)
    memberships = db.relationship('GymMembership', backref='customer', lazy=True)
    diet_plans = db.relationship('DietPlan', backref='customer', lazy=True)
    complaints = db.relationship('Complaint', backref='customer', lazy=True)
    
    def __repr__(self):
        return f'<Customer {self.FirstName} {self.LastName}>'

class EmergencyContact(db.Model):
    __tablename__ = 'emergency_contact'
    ContactID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    ContactName = db.Column(db.String(100))
    Relationship = db.Column(db.String(50))
    PhoneNumber = db.Column(db.String(20))

class CustomerFeedback(db.Model):
    __tablename__ = 'customer_feedback'
    FeedbackID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    Rating = db.Column(db.Integer)
    Comments = db.Column(db.Text)
    FeedbackDate = db.Column(db.Date)

class CustomerLog(db.Model):
    __tablename__ = 'customer_log'
    LogID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.Integer)
    FullName = db.Column(db.String(255))
    Action = db.Column(db.String(50))
    ActionTime = db.Column(db.DateTime)

class CustomerSupport(db.Model):
    __tablename__ = 'customer_support'
    TicketID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    Subject = db.Column(db.String(100))
    Description = db.Column(db.Text)
    Status = db.Column(db.String(50))
    CreatedAt = db.Column(db.DateTime)

# Employee related models
class GymEmployee(db.Model):
    __tablename__ = 'gymemployee'
    EmployeeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    GymID = db.Column(db.Integer, db.ForeignKey('gym.GymID'))
    
    # Relationships
    certifications = db.relationship('EmployeeCertification', backref='employee', lazy=True)
    attendances = db.relationship('EmployeeAttendance', backref='employee', lazy=True)
    salaries = db.relationship('Salary', backref='employee', lazy=True)
    
    def __repr__(self):
        return f'<Employee {self.FirstName} {self.LastName}>'

class EmployeeAttendance(db.Model):
    __tablename__ = 'employee_attendance'
    AttendanceID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('gymemployee.EmployeeID'))
    Date = db.Column(db.Date)
    CheckIn = db.Column(db.Time)
    CheckOut = db.Column(db.Time)

class EmployeeCertification(db.Model):
    __tablename__ = 'employee_certification'
    CertificationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('gymemployee.EmployeeID'))
    CertificationName = db.Column(db.String(100))
    IssuedBy = db.Column(db.String(100))
    IssueDate = db.Column(db.Date)
    ExpiryDate = db.Column(db.Date)

class GymManager(db.Model):
    __tablename__ = 'gymmanager'
    ManagerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    EmployeeID = db.Column(db.Integer, db.ForeignKey('gymemployee.EmployeeID'))
    
    # Relationships
    schedules = db.relationship('ManagerSchedule', backref='manager', lazy=True)

class ManagerSchedule(db.Model):
    __tablename__ = 'manager_schedule'
    ScheduleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ManagerID = db.Column(db.Integer, db.ForeignKey('gymmanager.ManagerID'))
    WorkDate = db.Column(db.Date)
    StartTime = db.Column(db.Time)
    EndTime = db.Column(db.Time)

# Gym related models
class Gym(db.Model):
    __tablename__ = 'gym'
    GymID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100))
    Address = db.Column(db.String(255))
    CustomerPhoneNumber = db.Column(db.String(15))
    
    # Relationships
    employees = db.relationship('GymEmployee', backref='gym', lazy=True)
    locations = db.relationship('Location', backref='gym', lazy=True)
    
    def __repr__(self):
        return f'<Gym {self.Name}>'

class Location(db.Model):
    __tablename__ = 'location'
    LocationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    GymID = db.Column(db.Integer, db.ForeignKey('gym.GymID'))
    FloorNumber = db.Column(db.Integer)
    RoomName = db.Column(db.String(100))
    Description = db.Column(db.Text)
    
    # Relationships
    maintenances = db.relationship('LocationMaintenance', backref='location', lazy=True)

class LocationMaintenance(db.Model):
    __tablename__ = 'location_maintenance'
    MaintenanceID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    LocationID = db.Column(db.Integer, db.ForeignKey('location.LocationID'))
    MaintenanceDate = db.Column(db.Date)
    PerformedBy = db.Column(db.String(100))
    Notes = db.Column(db.Text)

# Membership related models
class GymMembership(db.Model):
    __tablename__ = 'gymmembership'
    GymMembershipID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    
    # Relationships
    transactions = db.relationship('MembershipTransactionLog', backref='membership', lazy=True)

class CustomerMembership(db.Model):
    __tablename__ = 'customermembership'
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'), primary_key=True)
    GymMembershipID = db.Column(db.Integer, db.ForeignKey('gymmembership.GymMembershipID'), primary_key=True)

class SubscriptionPlan(db.Model):
    __tablename__ = 'subscription_plan'
    PlanID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PlanName = db.Column(db.String(50))
    DurationMonths = db.Column(db.Integer)
    Price = db.Column(db.Numeric(10, 2))

class MembershipTransactionLog(db.Model):
    __tablename__ = 'membership_transaction_log'
    TransactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    GymMembershipID = db.Column(db.Integer, db.ForeignKey('gymmembership.GymMembershipID'))
    TransactionDate = db.Column(db.Date)
    Status = db.Column(db.String(50))
    AmountPaid = db.Column(db.Numeric(10, 2))

# Class related models
class WorkoutClass(db.Model):
    __tablename__ = 'workoutclass'
    WorkoutClassID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    WorkoutClassName = db.Column(db.String(100))
    GymID = db.Column(db.Integer, db.ForeignKey('gym.GymID'))
    
    # Relationships
    sessions = db.relationship('ClassSession', backref='workout_class', lazy=True)
    prerequisites = db.relationship('ClassPrerequisite', backref='workout_class', lazy=True)
    equipment_requirements = db.relationship('ClassEquipmentRequirement', backref='workout_class', lazy=True)

class ClassSession(db.Model):
    __tablename__ = 'class_session'
    SessionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('gymemployee.EmployeeID'))
    WorkoutClassID = db.Column(db.Integer, db.ForeignKey('workoutclass.WorkoutClassID'))
    SessionDate = db.Column(db.Date)
    StartTime = db.Column(db.Time)
    EndTime = db.Column(db.Time)

class ClassPrerequisite(db.Model):
    __tablename__ = 'class_prerequisite'
    PrerequisiteID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    WorkoutClassID = db.Column(db.Integer, db.ForeignKey('workoutclass.WorkoutClassID'))
    Requirement = db.Column(db.String(100))

class ClassEquipmentRequirement(db.Model):
    __tablename__ = 'class_equipment_requirement'
    RequirementID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    GymID = db.Column(db.Integer, db.ForeignKey('gym.GymID'))
    WorkoutClassID = db.Column(db.Integer, db.ForeignKey('workoutclass.WorkoutClassID'))
    EquipmentName = db.Column(db.String(100))
    Quantity = db.Column(db.Integer)

class EmployeeTeachesClass(db.Model):
    __tablename__ = 'employeeteachesclass'
    EmployeeID = db.Column(db.Integer, db.ForeignKey('gymemployee.EmployeeID'), primary_key=True)
    WorkoutClassID = db.Column(db.Integer, db.ForeignKey('workoutclass.WorkoutClassID'), primary_key=True)

class GymHostsWorkoutClass(db.Model):
    __tablename__ = 'gymhostsworkoutclass'
    GymID = db.Column(db.Integer, db.ForeignKey('gym.GymID'), primary_key=True)
    WorkoutClassID = db.Column(db.Integer, db.ForeignKey('workoutclass.WorkoutClassID'), primary_key=True)

# Supplement related models
class Supplement(db.Model):
    __tablename__ = 'supplement'
    SupplementID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100))
    Brand = db.Column(db.String(100))
    Type = db.Column(db.String(50))
    Description = db.Column(db.Text)
    
    # Relationships
    stocks = db.relationship('SupplementStock', backref='supplement', lazy=True)
    customer_usages = db.relationship('SupplementUsageCustomer', backref='supplement', lazy=True)
    trainer_usages = db.relationship('SupplementUsageTrainer', backref='supplement', lazy=True)

class SupplementStock(db.Model):
    __tablename__ = 'supplement_stock'
    StockID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SupplementID = db.Column(db.Integer, db.ForeignKey('supplement.SupplementID'))
    GymID = db.Column(db.Integer, db.ForeignKey('gym.GymID'))
    Quantity = db.Column(db.Integer)
    LastRestocked = db.Column(db.Date)
    ExpiryDate = db.Column(db.Date)

class SupplementUsageCustomer(db.Model):
    __tablename__ = 'supplement_usage_customer'
    UsageID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SupplementID = db.Column(db.Integer, db.ForeignKey('supplement.SupplementID'))
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    StartDate = db.Column(db.Date)
    EndDate = db.Column(db.Date)
    Dosage = db.Column(db.String(50))

class SupplementUsageTrainer(db.Model):
    __tablename__ = 'supplement_usage_trainer'
    UsageID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SupplementID = db.Column(db.Integer, db.ForeignKey('supplement.SupplementID'))
    EmployeeID = db.Column(db.Integer, db.ForeignKey('gymemployee.EmployeeID'))
    StartDate = db.Column(db.Date)
    EndDate = db.Column(db.Date)
    Purpose = db.Column(db.Text)

# Financial related models
class Billing(db.Model):
    __tablename__ = 'billing'
    BillID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    Amount = db.Column(db.Numeric(10, 2))
    BillingDate = db.Column(db.Date)
    Description = db.Column(db.Text)

class PaymentMethod(db.Model):
    __tablename__ = 'payment_method'
    PaymentMethodID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    CardNumber = db.Column(db.String(20))
    ExpiryDate = db.Column(db.Date)
    CardType = db.Column(db.String(20))

class Salary(db.Model):
    __tablename__ = 'salary'
    SalaryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('gymemployee.EmployeeID'))
    Amount = db.Column(db.Numeric(10, 2))
    Month = db.Column(db.String(20))
    Year = db.Column(db.Integer)
    PaymentDate = db.Column(db.Date)

# Other models
class DietPlan(db.Model):
    __tablename__ = 'diet_plan'
    DietPlanID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    PlanDescription = db.Column(db.Text)
    StartDate = db.Column(db.Date)
    EndDate = db.Column(db.Date)

class Complaint(db.Model):
    __tablename__ = 'complaint'
    ComplaintID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'))
    ComplaintText = db.Column(db.Text)
    ComplaintDate = db.Column(db.Date)
    Status = db.Column(db.String(50))