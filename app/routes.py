from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required
from app.models import User, Unit
from app import db

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

    if request.method == "POST":

        username = request.form.get("username")

        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):

            login_user(user)

            return redirect(url_for("main.dashboard"))

    return render_template("auth/login.html")

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard/index.html")



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

        unit = Unit(

            code=request.form.get("code"),

            name=request.form.get("name"),

            address=request.form.get("address"),

            phone=request.form.get("phone"),

            email=request.form.get("email")

        )

        db.session.add(unit)

        db.session.commit()

        return redirect(url_for("main.units"))

    return render_template("units/add.html")