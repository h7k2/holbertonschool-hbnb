from flask_restx import Api, Resource
from flask import Blueprint

# Create API blueprint
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Configuration JWT pour Swagger
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT token. Format: Bearer <token>'
    }
}

api = Api(
    api_v1,
    version='1.0',
    title='HBnB API',
    description='HBnB Application API',
    authorizations=authorizations
    # security='Bearer'
)

# Imports des namespaces SEULEMENT
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns

# Enregistrer les namespaces
api.add_namespace(users_ns, path='/users')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')
api.add_namespace(amenities_ns, path='/amenities')

# Route de base
@api.route('/')
class HealthCheck(Resource):
    def get(self):
        """API Health Check"""
        return {
            'status': 'healthy',
            'message': 'HBnB API is running',
            'version': '1.0'
        }, 200

# PAS de facade ici !