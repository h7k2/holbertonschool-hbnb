from flask import Flask
from flask_restx import Api

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.setdefault("RESTX_MASK_SWAGGER", False)
    app.config.setdefault("ERROR_404_HELP", False)

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/",
    )