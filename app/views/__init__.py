from app.views.find_page import find_page_bp


def init_app(app):
    app.register_blueprint(find_page_bp)
