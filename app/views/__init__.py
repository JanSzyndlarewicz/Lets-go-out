from app.views.find_page import find_page_bp
from app.views.common import common_bp

def init_app(app):
    app.register_blueprint(find_page_bp)
    app.register_blueprint(common_bp)
