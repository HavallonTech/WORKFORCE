

from flask import Blueprint, app, current_app, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from app.models import Attendance, AuditLog, Department, User, Unit
from app import db
from app.helpers import toast
from app.utils.audit import log_audit
from app.models import UnitLocation
import re
from datetime import datetime, date
from app.utils.timezone import nigeria_now
import os
import base64
from app.utils.permissions import (
    admin_required,
    superadmin_required
)

from app.utils.geofence import (
    distance_in_meters
)
from io import BytesIO
import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)

from reportlab.lib import colors

from flask import send_file

from app.utils.field_attendance import (
    get_current_punch
)
from app.models import (
    FieldAttendance
)

main = Blueprint("main", __name__)



@main.before_app_request
def create_super_admin():

    if User.query.filter_by(role="superadmin").first():
        return

    admin = User(
        username="superadmin",
        email="kestplanet@gmail.com",
        role="superadmin"
    )

    admin.set_password("Admin@123")

    db.session.add(admin)

    db.session.commit()

    print("Super Admin Created")

@main.route("/", methods=["GET", "POST"])
def login():

    # User already logged in
    if current_user.is_authenticated:

        return redirect(
            url_for("main.dashboard")
        )

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )

        user = User.query.filter_by(
            username=username
        ).first()

        # if user.must_change_password:
        #     return redirect(
        #         url_for(
        #             "main.change_password"
        #         )
        #     )

        if user and user.check_password(password):

            user.last_login = nigeria_now()

            db.session.commit()

            login_user(user)

            log_audit(
                "Authentication",
                "Login",
                f"{user.username} logged in"
            )

            return redirect(
                url_for("main.dashboard")
            )

        else:

            toast(
                "Invalid username or password",
                "danger"
            )

    return render_template(
        "auth/login.html"
    )

@main.route("/dashboard")
@login_required
def dashboard():

    total_units = Unit.query.count()

    total_users = User.query.count()

    total_departments = Department.query.count()

    return render_template(
        "dashboard/index.html",
        total_units=total_units,
        total_users=total_users,
        total_departments=total_departments
    )



@main.route("/units")
@login_required
def units():

    units = Unit.query.order_by(Unit.name).all()

    return render_template(
        "units/list.html",
        units=units
    )

@main.route("/units/add", methods=["GET", "POST"])
@login_required
def add_unit():


    if request.method == "POST":

        code = request.form.get("code").strip().upper()

        existing = Unit.query.filter_by(
            code=code
        ).first()

        if existing:

            toast(
                "Unit code already exists",
                "warning"
            )

            return redirect(
                url_for("main.add_unit")
            )

        unit = Unit(
            code=code,
            name=request.form.get("name"),
            address=request.form.get("address"),
            phone=request.form.get("phone"),
            email=request.form.get("email")
        )

        db.session.add(unit)

        db.session.commit()
        log_audit(
            "Units",
            "Create Unit",
            f"Created Unit {unit.code}"
        )
        toast(
            "Unit created successfully",
            "success"
        )

        return redirect(url_for("main.units"))

    return render_template("units/add.html")

@main.route("/units/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_unit(id):

    unit = Unit.query.get_or_404(id)

    if request.method == "POST":

        unit.code =  request.form.get("code").strip().upper()

        unit.name = request.form.get("name")
        unit.address = request.form.get("address")
        unit.phone = request.form.get("phone")
        unit.email = request.form.get("email")

        db.session.commit()

        return redirect(url_for("main.units"))

    return render_template(
        "units/edit.html",
        unit=unit
    )

@main.route("/units/toggle/<int:id>")
@login_required
def toggle_unit(id):

    unit = Unit.query.get_or_404(id)

    unit.status = not unit.status

    db.session.commit()

    return redirect(url_for("main.units"))

@main.route("/test-toast")
def test_toast():

    flash(
        "WorkForce Toast System Working!",
        "success"
    )

    return redirect(
        url_for("main.dashboard")
    )

@main.route("/unit-locations")
@login_required
def unit_locations():

    locations = UnitLocation.query.order_by(
        UnitLocation.id.desc()
    ).all()
    total_locations = UnitLocation.query.count()

    active_locations = UnitLocation.query.filter_by(
        status=True
    ).count()

    inactive_locations = UnitLocation.query.filter_by(
        status=False
    ).count()

    return render_template(
        "unit_locations/list.html",
        locations=locations,
        total_locations=total_locations,
        active_locations=active_locations,
        inactive_locations=inactive_locations
    )

@main.route(
    "/unit-locations/add",
    methods=["GET", "POST"]
)
@login_required
def add_unit_location():

    units = Unit.query.filter_by(
        status=True
    ).all()

    if request.method == "POST":

        location = UnitLocation(

            unit_id=request.form.get(
                "unit_id"
            ),

            name=request.form.get(
                "name"
            ),

            latitude=request.form.get(
                "latitude"
            ),

            longitude=request.form.get(
                "longitude"
            ),

            radius=request.form.get(
                "radius"
            ),

            status=True
        )

        db.session.add(location)

        db.session.commit()

        log_audit(
            "Unit Locations",
            "Create Location",
            f"Created {location.name}"
        )

        toast(
            "Location added successfully",
            "success"
        )

        return redirect(
            url_for("main.unit_locations")
        )

    return render_template(
        "unit_locations/add.html",
        units=units
    )
@main.route("/unit-locations/toggle/<int:id>")
@login_required
def toggle_unit_location(id):

    location = UnitLocation.query.get_or_404(id)

    location.status = not location.status

    db.session.commit()

    log_audit(
        "Unit Locations",
        "Toggle Location",
        f"{location.name} status changed"
    )

    toast(
        "Location status updated",
        "info"
    )

    return redirect(
        url_for("main.unit_locations")
    )

@main.route(
    "/unit-locations/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_unit_location(id):

    location = UnitLocation.query.get_or_404(id)

    units = Unit.query.filter_by(
        status=True
    ).all()

    if request.method == "POST":

        location.unit_id = request.form.get(
            "unit_id"
        )

        location.name = request.form.get(
            "name"
        )

        location.latitude = request.form.get(
            "latitude"
        )

        location.longitude = request.form.get(
            "longitude"
        )

        location.radius = request.form.get(
            "radius"
        )

        db.session.commit()

        log_audit(
            "Unit Locations",
            "Edit Location",
            f"Updated {location.name}"
        )

        toast(
            "Location updated successfully",
            "success"
        )

        return redirect(
            url_for("main.unit_locations")
        )

    return render_template(
        "unit_locations/edit.html",
        location=location,
        units=units
    )

@main.route("/departments")
@login_required
def departments():

    departments = Department.query.order_by(
        Department.name
    ).all()

    return render_template(
        "departments/list.html",
        departments=departments
    )

@main.route(
    "/departments/add",
    methods=["GET", "POST"]
)
@login_required
def add_department():

    units = Unit.query.filter_by(
        status=True
    ).all()

    if request.method == "POST":

        department = Department(

            unit_id=request.form.get(
                "unit_id"
            ),

            name=request.form.get(
                "name"
            ),

            description=request.form.get(
                "description"
            ),

            status=True
        )

        db.session.add(department)

        db.session.commit()

        log_audit(
            "Departments",
            "Create Department",
            f"Created {department.name}"
        )

        toast(
            "Department created successfully",
            "success"
        )

        return redirect(
            url_for("main.departments")
        )

    return render_template(
        "departments/add.html",
        units=units
    )

@main.route(
    "/departments/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_department(id):

    department = Department.query.get_or_404(id)

    units = Unit.query.filter_by(
        status=True
    ).all()

    if request.method == "POST":

        department.unit_id = request.form.get(
            "unit_id"
        )

        department.name = request.form.get(
            "name"
        )

        department.description = request.form.get(
            "description"
        )

        db.session.commit()

        log_audit(
            "Departments",
            "Edit Department",
            f"Updated {department.name}"
        )

        toast(
            "Department updated successfully",
            "success"
        )

        return redirect(
            url_for("main.departments")
        )

    return render_template(
        "departments/edit.html",
        department=department,
        units=units
    )

@main.route("/departments/toggle/<int:id>")
@login_required
def toggle_department(id):

    department = Department.query.get_or_404(id)

    department.status = not department.status

    db.session.commit()

    log_audit(
        "Departments",
        "Toggle Department",
        f"{department.name} status changed"
    )

    toast(
        "Department status updated",
        "info"
    )

    return redirect(
        url_for("main.departments")
    )

@main.route("/users")
@login_required
def users():

    users = User.query.order_by(
        User.full_name
    ).all()

    total_users = User.query.count()

    active_users = User.query.filter_by(
        is_active_user=True
    ).count()

    inactive_users = User.query.filter_by(
        is_active_user=False
    ).count()

    return render_template(
        "users/list.html",
        users=users,
        total_users=total_users,
        active_users=active_users,
        inactive_users=inactive_users
    )
@main.route(
    "/users/add",
    methods=["GET", "POST"]
)
@login_required
def add_user():

    units = Unit.query.filter_by(
        status=True
    ).all()

    departments = Department.query.filter_by(
        status=True
    ).all()

    if request.method == "POST":
        #######################################################################
        #####################User Validation##################################
        email = request.form.get("email").strip()

        email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.match(email_pattern, email):

            toast(
                "Please enter a valid email address",
                "warning"
            )

            return redirect(
                url_for("main.add_user")
            )

        existing_username = User.query.filter_by(
            username=request.form.get("username")
        ).first()

        if existing_username:

            toast(
                "Username already exists",
                "warning"
            )

            return redirect(
                url_for("main.add_user")
            )

        existing_email = User.query.filter_by(
            email=request.form.get("email")
        ).first()

        if existing_email:

            toast(
                "Email already in use by another user",
                "warning"
            )

            return redirect(
                url_for("main.add_user")
            )

        if request.form.get("password") != request.form.get(
            "confirm_password"
        ):

            toast(
                "Passwords do not match",
                "warning"
            )

            return redirect(
                url_for("main.add_user")
            )
        #########################################################################
        user = User(

            staff_id=request.form.get(
                "staff_id"
            ),

            full_name=request.form.get(
                "full_name"
            ),

            username=request.form.get(
                "username"
            ),

            email=request.form.get(
                "email"
            ),

            phone=request.form.get(
                "phone"
            ),

            unit_id=request.form.get(
                "unit_id"
            ),

            department_id=request.form.get(
                "department_id"
            ),

            role=request.form.get(
                "role"
            )
        )

        user.set_password(
            request.form.get(
                "password"
            )
        )

        db.session.add(user)

        db.session.commit()

        log_audit(
            "Users",
            "Create User",
            f"Created user {user.username}"
        )

        toast(
            "User created successfully",
            "success"
        )

        return redirect(
            url_for("main.users")
        )

    return render_template(
        "users/add.html",
        units=units,
        departments=departments
    )

##################################Edit a User Route##########################################
@main.route(
    "/users/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_user(id):

    user = User.query.get_or_404(id)

    units = Unit.query.filter_by(
        status=True
    ).all()

    departments = Department.query.filter_by(
        status=True
    ).all()

    if request.method == "POST":

        existing_email = User.query.filter(
            User.email == request.form.get("email"),
            User.id != user.id
        ).first()

        ####################################################################################
        email = request.form.get("email").strip()

        email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.match(email_pattern, email):

            toast(
                "Please enter a valid email address",
                "warning"
            )

            return redirect(
                url_for(
                    "main.edit_user",
                    id=id
                )
            )
        ################################################################################

        if existing_email:

            toast(
                "Email already exists",
                "warning"
            )

            return redirect(
                url_for(
                    "main.edit_user",
                    id=id
                )
            )

        user.staff_id = request.form.get(
            "staff_id"
        )

        user.full_name = request.form.get(
            "full_name"
        )

        user.username = request.form.get(
            "username"
        )

        user.email = request.form.get(
            "email"
        )

        user.phone = request.form.get(
            "phone"
        )

        user.unit_id = request.form.get(
            "unit_id"
        )

        user.department_id = request.form.get(
            "department_id"
        )

        user.role = request.form.get(
            "role"
        )

        db.session.commit()

        log_audit(
            "Users",
            "Edit User",
            f"Updated {user.username}"
        )

        toast(
            "User updated successfully",
            "success"
        )

        return redirect(
            url_for("main.users")
        )

    return render_template(
        "users/edit.html",
        user=user,
        units=units,
        departments=departments
    )

@main.route("/users/toggle/<int:id>")
@login_required
def toggle_user(id):

    user = User.query.get_or_404(id)

    user.is_active_user = (
        not user.is_active_user
    )

    db.session.commit()

    log_audit(
        "Users",
        "Toggle User",
        f"{user.username} status changed"
    )

    toast(
        "User status updated",
        "info"
    )

    return redirect(
        url_for("main.users")
    )


@main.route("/logout")
@login_required
def logout():

    log_audit(
        "Authentication",
        "Logout",
        f"{current_user.username} logged out"
    )

    logout_user()

    toast(
        "Logged out successfully",
        "success"
    )

    return redirect(
        url_for("main.login")
    )

@main.route(
    "/change-password",
    methods=["GET", "POST"]
)
@login_required
def change_password():

    if request.method == "POST":

        current_password = request.form.get(
            "current_password"
        )

        new_password = request.form.get(
            "new_password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )

        if not current_user.check_password(
            current_password
        ):

            toast(
                "Current password is incorrect",
                "warning"
            )

            return redirect(
                url_for(
                    "main.change_password"
                )
            )

        if new_password != confirm_password:

            toast(
                "Passwords do not match",
                "warning"
            )

            return redirect(
                url_for(
                    "main.change_password"
                )
            )

        if len(new_password) < 8:

            toast(
                "Password must be at least 8 characters",
                "warning"
            )

            return redirect(
                url_for(
                    "main.change_password"
                )
            )

        current_user.set_password(
            new_password
        )

        current_user.must_change_password = False

        db.session.commit()

        log_audit(
            "Authentication",
            "Change Password",
            f"{current_user.username} changed password"
        )

        logout_user()

        toast(
            "Password changed successfully. Please login again.",
            "success"
        )

        return redirect(
            url_for("main.login")
        )
    return render_template(
        "auth/change_password.html"
    )

@main.route("/profile")
@login_required
def profile():

    return render_template(
        "auth/profile.html"
    )

@main.route("/attendance")
@login_required
def my_attendance():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    records = query.order_by(
        Attendance.attendance_date.desc(),
        Attendance.id.desc()
    ).paginate(
        page=page,
        per_page=20,
        error_out=False
    )

    return render_template(
        "attendance/list.html",
        records=records
    )

#####################################################Check in Route########################################################

@main.route(
    "/attendance/check-in",
    methods=["GET", "POST"]
)
@login_required
def check_in():

    today = nigeria_now().date()

    if request.method == "POST":

        existing = Attendance.query.filter_by(
            user_id=current_user.id,
            attendance_date=today
        ).first()

        if existing:

            toast(
                "You have already checked in today",
                "warning"
            )

            return redirect(
                url_for("main.my_attendance")
            )

        if not current_user.unit_id:

            toast(
                "You are not assigned to any unit",
                "warning"
            )

            return redirect(
                url_for("main.dashboard")
            )

        # ==========================================
        # GPS CAPTURE
        # ==========================================

        check_in_latitude = request.form.get(
            "latitude"
        )

        check_in_longitude = request.form.get(
            "longitude"
        )

        if not check_in_latitude or not check_in_longitude:

            toast(
                "Location is required for attendance",
                "warning"
            )

            return redirect(
                url_for("main.check_in")
            )

        # ==========================================
        # GEOFENCE VALIDATION
        # ==========================================

        active_locations = UnitLocation.query.filter_by(
            unit_id=current_user.unit_id,
            status=True
        ).all()

        if not active_locations:

            toast(
                "No active attendance location configured for your unit",
                "danger"
            )

            return redirect(
                url_for("main.my_attendance")
            )

        allowed = False

        matched_location = None

        matched_distance = None

        for location in active_locations:

            distance = distance_in_meters(

                check_in_latitude,
                check_in_longitude,

                location.latitude,
                location.longitude
            )

            if distance <= location.radius:

                allowed = True

                matched_location = location

                matched_distance = distance

                break

        if not allowed:

            toast(
                "You are outside all approved attendance locations",
                "danger"
            )

            return redirect(
                url_for("main.my_attendance")
            )

        # ==========================================
        # SELFIE CAPTURE
        # ==========================================

        photo_data = request.form.get(
            "photo"
        )

        filename = None

        if photo_data:

            upload_folder = os.path.join(
                "app",
                "static",
                "uploads",
                "attendance"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            filename = (
                f"checkin_"
                f"{current_user.id}_"
                f"{today}.jpg"
            )

            filepath = os.path.join(
                upload_folder,
                filename
            )

            try:

                header, encoded = photo_data.split(
                    ",",
                    1
                )

                with open(
                    filepath,
                    "wb"
                ) as f:

                    f.write(
                        base64.b64decode(
                            encoded
                        )
                    )

            except Exception as e:

                toast(
                    f"Photo save failed: {e}",
                    "danger"
                )

                return redirect(
                    url_for(
                        "main.check_in"
                    )
                )

        # ==========================================
        # SAVE ATTENDANCE
        # ==========================================

        attendance = Attendance(

            user_id=current_user.id,

            unit_id=current_user.unit_id,

            location_id=matched_location.id,

            attendance_date=today,

            check_in=nigeria_now(),

            check_in_photo=filename,

            check_in_latitude=check_in_latitude,

            check_in_longitude=check_in_longitude,

            status="Present"
        )

        db.session.add(
            attendance
        )

        db.session.commit()

        # ==========================================
        # AUDIT LOG
        # ==========================================

        log_audit(
            "Attendance",
            "Check In",
            f"{current_user.username} checked in "
            f"{round(matched_distance)}m from "
            f"{matched_location.name}"
        )

        toast(
            "Check in successful",
            "success"
        )

        return redirect(
            url_for("main.my_attendance")
        )

    return render_template(
        "attendance/check_in.html"
    )

@main.route(
    "/attendance/check-out",
    methods=["GET", "POST"]
)

##########################################################################Check out Route#####################################################################
##############################################################################################################################################
@main.route(
    "/attendance/check-out",
    methods=["GET", "POST"]
)
@login_required
def check_out():

    today = nigeria_now().date()

    attendance = Attendance.query.filter_by(
        user_id=current_user.id,
        attendance_date=today
    ).order_by(
        Attendance.id.desc()
    ).first()

    if not attendance:

        toast(
            "You must check in first",
            "warning"
        )

        return redirect(
            url_for("main.my_attendance")
        )

    if request.method == "POST":

        if attendance.check_out:

            toast(
                "Already checked out",
                "warning"
            )

            return redirect(
                url_for("main.my_attendance")
            )

        # ==========================================
        # GPS CAPTURE
        # ==========================================

        check_out_latitude = request.form.get(
            "latitude"
        )

        check_out_longitude = request.form.get(
            "longitude"
        )

        if not check_out_latitude or not check_out_longitude:

            toast(
                "Location is required for check out. Kindly allow location access and try again.",
                "warning"
            )

            return redirect(
                url_for("main.check_out")
            )

        # ==========================================
        # GEOFENCE VALIDATION
        # ==========================================

        active_locations = UnitLocation.query.filter_by(
            unit_id=current_user.unit_id,
            status=True
        ).all()

        if not active_locations:

            toast(
                "No active attendance location configured for your unit",
                "danger"
            )

            return redirect(
                url_for("main.my_attendance")
            )

        allowed = False

        matched_location = None

        matched_distance = None

        for location in active_locations:

            distance = distance_in_meters(

                check_out_latitude,
                check_out_longitude,

                location.latitude,
                location.longitude
            )

            if distance <= location.radius:

                allowed = True

                matched_location = location

                matched_distance = distance

                break

        if not allowed:

            toast(
                "You are outside all approved attendance locations",
                "danger"
            )

            return redirect(
                url_for("main.my_attendance")
            )

        # ==========================================
        # SELFIE CAPTURE
        # ==========================================

        photo_data = request.form.get(
            "photo"
        )

        filename = None

        if photo_data:

            upload_folder = os.path.join(
                "app",
                "static",
                "uploads",
                "attendance"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            filename = (
                f"checkout_"
                f"{current_user.id}_"
                f"{today}.jpg"
            )

            filepath = os.path.join(
                upload_folder,
                filename
            )

            try:

                header, encoded = photo_data.split(
                    ",",
                    1
                )

                with open(
                    filepath,
                    "wb"
                ) as f:

                    f.write(
                        base64.b64decode(
                            encoded
                        )
                    )

            except Exception as e:

                toast(
                    f"Photo save failed: {e}",
                    "danger"
                )

                return redirect(
                    url_for(
                        "main.check_out"
                    )
                )

        # ==========================================
        # SAVE CHECK OUT
        # ==========================================

        attendance.check_out = nigeria_now()

        attendance.check_out_photo = filename

        attendance.check_out_latitude = (
            check_out_latitude
        )

        attendance.check_out_longitude = (
            check_out_longitude
        )

        db.session.commit()

        # ==========================================
        # AUDIT LOG
        # ==========================================

        log_audit(
            "Attendance",
            "Check Out",
            f"{current_user.username} checked out "
            f"{round(matched_distance)}m from "
            f"{matched_location.name}"
        )

        toast(
            "Check out successful",
            "success"
        )

        return redirect(
            url_for("main.my_attendance")
        )

    return render_template(
        "attendance/check_out.html"
    )

#######################Reusable Filter Block for Attendance Report Route############################################################
###############################################################################################################################

def get_attendance_query():

    query = Attendance.query

    start_date = request.args.get(
        "start_date"
    )

    end_date = request.args.get(
        "end_date"
    )

    unit_id = request.args.get(
        "unit_id"
    )

    user_id = request.args.get(
        "user_id"
    )

    if start_date:

        query = query.filter(
            Attendance.attendance_date >= start_date
        )

    if end_date:

        query = query.filter(
            Attendance.attendance_date <= end_date
        )

    if unit_id:

        query = query.filter(
            Attendance.unit_id == unit_id
        )

    if user_id:

        query = query.filter(
            Attendance.user_id == user_id
        )

    return query


###################################################################################################333333333333333
#############################Attendance Report Route########################################################################################
@main.route(
    "/reports/attendance",
    methods=["GET"]
)
@login_required
def attendance_report():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    start_date = request.values.get(
        "start_date"
    )

    end_date = request.values.get(
        "end_date"
    )

    unit_id = request.values.get(
        "unit_id"
    )

    user_id = request.values.get(
        "user_id"
    )

    units = Unit.query.filter_by(
        status=True
    ).all()

    users = User.query.filter_by(
        is_active_user=True
    ).all()

    query = Attendance.query

    if start_date:

        query = query.filter(
            Attendance.attendance_date >= start_date
        )

    if end_date:

        query = query.filter(
            Attendance.attendance_date <= end_date
        )

    if unit_id:

        query = query.filter(
            Attendance.unit_id == unit_id
        )

    if user_id:

        query = query.filter(
            Attendance.user_id == user_id
        )

    records = query.order_by(

        Attendance.attendance_date.desc(),

        Attendance.id.desc()

    ).paginate(

        page=page,

        per_page=20,

        error_out=False

    )

    if start_date or end_date or unit_id or user_id:

        log_audit(
            "Reports",
            "Attendance Report",
            "Attendance report generated"
        )

    return render_template(

        "reports/attendance.html",

        records=records,

        start_date=start_date,

        end_date=end_date,

        unit_id=unit_id,

        user_id=user_id,

        units=units,

        users=users
    )




@main.route("/audit-logs",methods=["GET", "POST"])
@login_required
@superadmin_required
def audit_logs():

    users = User.query.order_by(
        User.full_name
    ).all()

    modules = db.session.query(
        AuditLog.module
    ).distinct().all()

    query = AuditLog.query
    total_logs = AuditLog.query.count()

    today_logs = AuditLog.query.filter(
        db.func.date(
            AuditLog.created_at
        ) == nigeria_now().date()
    ).count()

    total_users = db.session.query(
        AuditLog.username
    ).distinct().count()

    total_modules = db.session.query(
        AuditLog.module
    ).distinct().count()

    start_date = None
    end_date = None
    user_id = None
    module = None

    if request.method == "POST":

        start_date = request.form.get(
            "start_date"
        )

        end_date = request.form.get(
            "end_date"
        )

        user_id = request.form.get(
            "user_id"
        )

        module = request.form.get(
            "module"
        )

        if start_date:

            query = query.filter(
                db.func.date(
                    AuditLog.created_at
                ) >= start_date
            )

        if end_date:

            query = query.filter(
                db.func.date(
                    AuditLog.created_at
                ) <= end_date
            )

        if user_id:

            query = query.filter(
                AuditLog.user_id == int(user_id)
            )

        if module:

            query = query.filter(
                AuditLog.module == module
            )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    logs = query.order_by(
        AuditLog.id.desc()
    ).paginate(
        page=page,
        per_page=50
    )

    return render_template(
        "audit_logs/list.html",
        logs=logs,
        users=users,
        modules=modules,
        start_date=start_date,
        end_date=end_date,
        selected_user=user_id,
        total_logs=total_logs,
        today_logs=today_logs,
        total_users=total_users,
        total_modules=total_modules,
        selected_module=module
    )

@main.route(
    "/audit-logs/excel"
)
@login_required
@superadmin_required
def export_audit_excel():

    logs = AuditLog.query.order_by(
        AuditLog.id.desc()
    ).all()

    data = []

    for log in logs:

        data.append({

            "Date Time":
            log.created_at,

            "User":
            log.username,

            "Module":
            log.module,

            "Action":
            log.action,

            "Details":
            log.details,

            "IP Address":
            log.ip_address
        })

    df = pd.DataFrame(data)

    output = BytesIO()

    df.to_excel(
        output,
        index=False
    )

    output.seek(0)

    return send_file(

        output,

        download_name=
        "audit_logs.xlsx",

        as_attachment=True
    )
@main.route(
    "/audit-logs/pdf"
)
@login_required
@admin_required
def export_audit_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    data = [[

        "Date",

        "User",

        "Module",

        "Action"

    ]]

    logs = AuditLog.query.order_by(
        AuditLog.id.desc()
    ).all()

    for log in logs:

        data.append([

            str(log.created_at),

            log.username or "",

            log.module or "",

            log.action or ""

        ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightblue
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )

    doc.build(
        [table]
    )

    buffer.seek(0)

    return send_file(

        buffer,

        as_attachment=True,

        download_name=
        "audit_logs.pdf",

        mimetype=
        "application/pdf"
    )

from datetime import datetime

@main.route(
    "/audit-logs/print"
)
@login_required
@admin_required
def print_audit_logs():

    logs = AuditLog.query.order_by(
        AuditLog.id.desc()
    ).all()

    return render_template(

        "audit_logs/print.html",

        logs=logs,

        generated_at=datetime.now().strftime(
            "%d-%b-%Y %H:%M"
        )
    )



@main.route("/reports/attendance/print")
@login_required
@admin_required
def print_attendance_report():

    records = get_attendance_query().order_by(
        Attendance.attendance_date.desc()
        ).all()

    generated_at = datetime.now().strftime(
        "%d-%b-%Y %I:%M %p"
    )
    return render_template(
        "reports/attendance_print.html",
        records=records,
        generated_at=generated_at
    )

@main.route(
    "/reports/attendance/excel"
)
@login_required
@admin_required
def export_attendance_excel():

    records = get_attendance_query().order_by(
        Attendance.attendance_date.desc()
        ).all()

    data = []

    for record in records:

        data.append({

            "Date":
            record.attendance_date,

            "Staff":
            record.user.full_name,

            "Unit":
            record.unit.name,

            "Location":
            record.location.name
            if record.location
            else "",

            "Check In":
            record.check_in,

            "Check Out":
            record.check_out,

            "Status":
            record.status,

            "Check In Latitude":
            record.check_in_latitude,

            "Check In Longitude":
            record.check_in_longitude,

            "Check Out Latitude":
            record.check_out_latitude,

            "Check Out Longitude":
            record.check_out_longitude
        })

    df = pd.DataFrame(data)

    output = BytesIO()

    df.to_excel(
        output,
        index=False
    )

    output.seek(0)

    return send_file(

        output,

        download_name=
        "attendance_report.xlsx",

        as_attachment=True
    )

@main.route(
    "/reports/attendance/pdf"
)
@login_required
@admin_required
def export_attendance_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    data = [[

        "Date",

        "Staff",

        "Unit",

        "Location",

        "Status"

    ]]

    records = get_attendance_query().order_by(
        Attendance.attendance_date.desc()
    ).all()

    for record in records:

        data.append([

            str(
                record.attendance_date
            ),

            record.user.full_name,

            record.unit.name,

            record.location.name
            if record.location
            else "",

            record.status

        ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightblue
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            )
        ])
    )

    doc.build(
        [table]
    )

    buffer.seek(0)

    return send_file(

        buffer,

        download_name=
        "attendance_report.pdf",

        as_attachment=True,

        mimetype=
        "application/pdf"
    )

@main.route(
    "/field-attendance/checkpoint",
    methods=["GET", "POST"]
)
@login_required
def field_checkpoint():

    today = nigeria_now().date()

    current_time = nigeria_now().time()

    current_punch = get_current_punch(
        current_time
    )

    if not current_punch:

        toast(
            "No active attendance window currently, its late.",
            "warning"
        )

        return redirect(
            url_for(
                "main.dashboard"
            )
        )

    existing = FieldAttendance.query.filter_by(

        user_id=current_user.id,

        attendance_date=today,

        checkpoint_number=current_punch

    ).first()

    if existing:

        toast(
            f"Punch {current_punch} already recorded",
            "warning"
        )

        return redirect(
            url_for(
                "main.dashboard"
            )
        )

    if request.method == "POST":

        photo_data = request.form.get(
            "photo"
        )

        latitude = request.form.get(
            "latitude"
        )

        longitude = request.form.get(
            "longitude"
        )

        remarks = request.form.get(
            "remarks"
        )

        if not latitude or not longitude:

            toast(
                "Location required",
                "danger"
            )

            return redirect(
                url_for(
                    "main.field_checkpoint"
                )
            )

        active_locations = UnitLocation.query.filter_by(

            unit_id=current_user.unit_id,

            status=True

        ).all()

        if not active_locations:

            toast(
                "No attendance location configured",
                "danger"
            )

            return redirect(
                url_for(
                    "main.dashboard"
                )
            )

        allowed = False

        matched_location = None

        matched_distance = None

        for location in active_locations:

            distance = distance_in_meters(

                float(latitude),

                float(longitude),

                location.latitude,

                location.longitude

            )

            if distance <= location.radius:

                allowed = True

                matched_location = location

                matched_distance = distance

                break

        if not allowed:

            toast(
                "You are outside all approved attendance locations",
                "danger"
            )

            return redirect(
                url_for(
                    "main.field_checkpoint"
                )
            )
        
        if not photo_data:
            toast(
                "Selfie is required",
                "danger"
                )
            return redirect(
                    url_for(
                        "main.field_checkpoint"
                    )
                )

        upload_folder = os.path.join(

            "app",

            "static",

            "uploads",

            "field_attendance"

        )

        os.makedirs(

            upload_folder,

            exist_ok=True

        )

        filename = (

            f"field_"

            f"{current_user.id}_"

            f"{today}_"

            f"{current_punch}.jpg"

        )

        filepath = os.path.join(

            upload_folder,

            filename

        )

        header, encoded = photo_data.split(
            ",",
            1
        )

        with open(
            filepath,
            "wb"
        ) as f:

            f.write(
                base64.b64decode(
                    encoded
                )
            )
        attendance = FieldAttendance(

            user_id=current_user.id,

            unit_id=current_user.unit_id,

            location_id=matched_location.id,

            attendance_date=today,

            checkpoint_number=current_punch,

            attendance_time=nigeria_now(),

            photo=filename,

            latitude=float(latitude),

            longitude=float(longitude),

            distance=matched_distance,

            remarks=remarks

        )

        db.session.add(
            attendance
        )

        db.session.commit()

        log_audit(

            "Field Attendance",

            f"Punch {current_punch}",

            f"{current_user.username} completed Punch {current_punch} "
            f"at {matched_location.name} "
            f"({round(matched_distance,2)}m)"
        )

        toast(

            f"Punch {current_punch} recorded successfully",

            "success"

        )

        return redirect(
            url_for(
                "main.dashboard"
            )
        )

    today_count = FieldAttendance.query.filter_by(

        user_id=current_user.id,

        attendance_date=today

    ).count()

    return render_template(

        "field_attendance/checkpoint.html",

        current_punch=current_punch,

        completed=today_count,

        remaining=8 - today_count
    )