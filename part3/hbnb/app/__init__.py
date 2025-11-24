from flask import Flask, jsonify
from flask_restx import Api
from app.extensions import db, bcrypt, jwt

def create_app(config_class='config.DevelopmentConfig'):
    """
    Application Factory pattern
    Creates and configures the Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    if isinstance(config_class, str):
        app.config.from_object(config_class)
    else:
        app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Enable CORS for all routes (allow frontend requests)
    from flask_cors import CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # JWT error handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({
            'error': 'Missing or invalid token',
            'message': 'Request does not contain a valid token'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({
            'error': 'Invalid token',
            'message': 'Token verification failed'
        }), 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token expired',
            'message': 'The token has expired'
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token revoked',
            'message': 'The token has been revoked'
        }), 401
    
    # Create API instance with authorization configuration
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Bearer token. Format: Bearer <token>'
        }
    }
    
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API with JWT Authentication',
        doc='/',
        prefix='/api/v1',
        authorizations=authorizations
    )

    # Import and register namespaces
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns

    # Register namespaces
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(reviews_ns, path='/reviews')
    api.add_namespace(amenities_ns, path='/amenities')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
