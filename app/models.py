from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    staff_id = db.Column(
        db.String(50),
        unique=True,
        nullable=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    full_name = db.Column(
        db.String(150),
        nullable=True
    )

    email = db.Column(
        db.String(120),
        unique=True
    )

    phone = db.Column(
        db.String(20)
    )

    unit_id = db.Column(
        db.Integer,
        db.ForeignKey("units.id"),
        nullable=True
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=True
    )

    password_hash = db.Column(
        db.String(255)
    )

    role = db.Column(
        db.String(30),
        default="staff"
    )

    is_active_user = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
    last_login = db.Column(
        db.DateTime,
        nullable=True
    )
    must_change_password = db.Column(
        db.Boolean,
        default=True
    )
    attendances = db.relationship(
        "Attendance",
        backref="user",
        lazy=True
    )
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )
    
    
class Unit(db.Model):

    __tablename__ = "units"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(
        db.String(20),
        unique=True
    )

    name = db.Column(
        db.String(100)
    )

    address = db.Column(
        db.Text
    )

    phone = db.Column(
        db.String(20)
    )

    email = db.Column(
        db.String(120)
    )

    status = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
    locations = db.relationship(
        "UnitLocation",
        backref="unit",
        lazy=True
    )
    departments = db.relationship(
        "Department",
        backref="unit",
        lazy=True
    )
    users = db.relationship(
        "User",
        backref="unit",
        lazy=True
    )
    attendances = db.relationship(
        "Attendance",
        backref="unit",
        lazy=True
    )
    


class UnitLocation(db.Model):

    __tablename__ = "unit_locations"

    id = db.Column(db.Integer, primary_key=True)

    unit_id = db.Column(
        db.Integer,
        db.ForeignKey("units.id")
    )

    name = db.Column(db.String(100))

    latitude = db.Column(db.Float)

    longitude = db.Column(db.Float)

    radius = db.Column(db.Integer, default=100)
    status = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
    attendances = db.relationship(
        "Attendance",
        backref="location",
        lazy=True
    )
        
    

class Department(db.Model):

    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)

    unit_id = db.Column(
        db.Integer,
        db.ForeignKey("units.id")
    )

    name = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.Text
    )
    status = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
    users = db.relationship(
        "User",
        backref="department",
        lazy=True
    )

class Attendance(db.Model):

    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    unit_id = db.Column(
        db.Integer,
        db.ForeignKey("units.id")
    )

    check_in = db.Column(db.DateTime)

    check_out = db.Column(db.DateTime)

    latitude = db.Column(db.Float)

    longitude = db.Column(db.Float)

    status = db.Column(db.String(20))

    attendance_date = db.Column(db.Date)
    location_id = db.Column(
        db.Integer,
        db.ForeignKey("unit_locations.id"),
        nullable=True
    )

    remarks = db.Column(
        db.String(255),
        nullable=True
    )
    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
    check_in_photo = db.Column(
        db.String(255),
        nullable=True
    )

    check_out_photo = db.Column(
        db.String(255),
        nullable=True
    )
    check_in_latitude = db.Column(
        db.Float,
        nullable=True
    )

    check_in_longitude = db.Column(
        db.Float,
        nullable=True
    )

    check_out_latitude = db.Column(
        db.Float,
        nullable=True
    )

    check_out_longitude = db.Column(
        db.Float,
        nullable=True
    )
    
class AuditLog(db.Model):

    __tablename__ = "audit_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    username = db.Column(
        db.String(100)
    )

    action = db.Column(
        db.String(200)
    )

    module = db.Column(
        db.String(100)
    )

    details = db.Column(
        db.Text
    )

    ip_address = db.Column(
        db.String(50)
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )