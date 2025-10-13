from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    app.config.setdefault("RESTX_MASK_SWAGGER", False)
    app.config.setdefault("ERROR_404_HELP", False)