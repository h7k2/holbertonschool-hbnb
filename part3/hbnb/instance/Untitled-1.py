# Importer les namespaces (= groupes d'endpoints)
from app.api.v1.users import api as users_ns      # Endpoints /users/
from app.api.v1.places import api as places_ns    # Endpoints /places/
from app.api.v1.reviews import api as reviews_ns  # Endpoints /reviews/
from app.api.v1.amenities import api as amenities_ns  # Endpoints /amenities/

# Créer le blueprint (= groupe de routes Flask)
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Configuration JWT pour Swagger (le cadenas 🔒)
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT token. Format: Bearer <token>'
    }
}

# Créer l'API Swagger avec JWT
api = Api(
    api_v1,
    version='1.0',
    title='HBnB API',  # Titre dans Swagger
    description='HBnB Application API',
    authorizations=authorizations,  # Active le bouton 🔒 Authorize
    security='Bearer'  # Active JWT par défaut
)

# Enregistrer les endpoints dans Swagger
api.add_namespace(users_ns, path='/users')      # → /api/v1/users/
api.add_namespace(places_ns, path='/places')    # → /api/v1/places/
api.add_namespace(reviews_ns, path='/reviews')  # → /api/v1/reviews/
api.add_namespace(amenities_ns, path='/amenities')  # → /api/v1/amenities/