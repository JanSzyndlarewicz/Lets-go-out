from flask import Flask

from app.extensions import login_manager
from app.models import User, db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.secret_key = "secret_key"  # TODO: Change this to a random value

    # Configure database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)

    # Register blueprints
    from app.auth import auth_bp

    app.register_blueprint(auth_bp)

    from app.dashboard import dashboard_bp

    app.register_blueprint(dashboard_bp)

    return app
