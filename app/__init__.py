from flask import Flask
from flask_apscheduler import APScheduler
from flask_login import LoginManager
from flask_mail import Mail

from app.models import User
from app.models.database import db
from app.utils.jobs import delete_rejects


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    app.mail = Mail(app)

    # Initialize extensions
    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.scheduler = APScheduler()
    app.scheduler.init_app(app)
    app.scheduler.add_job("delete_rejects", lambda : delete_rejects(app), trigger="interval", days=1)
    app.scheduler.start()

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

    from app.views.common import common_bp

    app.register_blueprint(common_bp)

    from app.views.profile import profile_bp

    app.register_blueprint(profile_bp)

    from app.views.interaction import interaction_bp

    app.register_blueprint(interaction_bp)

    return app

