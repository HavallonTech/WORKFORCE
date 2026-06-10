from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()

migrate = Migrate()

login_manager = LoginManager()

login_manager.login_view = "login"


def create_app():

    app = Flask(__name__)

    app.config.from_object(
        "config.Config"
    )

    app.config[
        "TEMPLATES_AUTO_RELOAD"
    ] = True

    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(
            int(user_id)
        )

    from app.routes import main

    app.register_blueprint(
        main
    )

    @app.errorhandler(403)
    def forbidden(error):

        return render_template(
            "errors/403.html"
        ), 403

    return app