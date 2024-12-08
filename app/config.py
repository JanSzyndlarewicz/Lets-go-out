SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "secret_key"

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USERNAME = "webapp2024madrid@gmail.com"
MAIL_PASSWORD = "eshkswvewdvzrcnw"
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = "webapp2024madrid@gmail.com"

ADVANCED_ACCESS_CONTROL = False

#Set this to something reasonable like 8 for the final version
MINIMUM_PASSWORD_LENGTH = 1
MAXIMUM_MESSAGE_LENGTH = 512

UPLOAD_FOLDER = "app/static/images"

MAIN_PAGE_ROUTE = "find_page_bp.find_page_invite"
UNCONFIRMED_PAGE_ROUTE = "auth_bp.unconfirmed"
LOGIN_PAGE_ROUTE = "auth_bp.login"

INITIAL_SUGGESTION_NUMBER = 15
REFILL_SUGGESTION_NUMBER = 10

DEFAULT_PHOTO = "images/default-profile-picture.jpg"

REJECT_DAYS_DURATION = 3
