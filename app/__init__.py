from flask import Flask
from flask_login import LoginManager

from app.models import User, db


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

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.views.auth import auth_bp

    app.register_blueprint(auth_bp)

    from app.views.you_page import you_page_bp

    app.register_blueprint(you_page_bp)

    from app.views.matches_page import matches_page_bp

    app.register_blueprint(matches_page_bp)

    from app.views.about_us_page import about_us_page_bp

    app.register_blueprint(about_us_page_bp)

    from app.views.find_page import find_page_bp

    app.register_blueprint(find_page_bp)

    from app.views.profile_manager import profile_manager_bp

    app.register_blueprint(profile_manager_bp)

    from app.views.profile import profile_bp

    app.register_blueprint(profile_bp)

    return app
