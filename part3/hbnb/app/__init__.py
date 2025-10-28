from flask import Flask
from flask_bcrypt import Bcrypt
from config import DevelopmentConfig  # Adjust path as needed

bcrypt = Bcrypt()  # Instantiate Bcrypt

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    bcrypt.init_app(app)

    # Register blueprints, routes, etc.
    from app.api.v1.users.routes import users_bp
    app.register_blueprint(users_bp, url_prefix="/api/v1/users")

    return app
