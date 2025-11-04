from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Model for login response
token_response_model = api.model('TokenResponse', {
    'access_token': fields.String(description='JWT access token'),
    'user': fields.Raw(description='User information')
})

facade = HBnBFacade()

@api.route('/login')
class Login(Resource):
    @api.doc('user_login')
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful', token_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """
        Authenticate user and return JWT token
        """
        credentials = api.payload
        
        # Validate input
        if not credentials.get('email') or not credentials.get('password'):
            api.abort(400, 'Email and password are required')
        
        # Get user by email
        user = facade.get_user_by_email(credentials['email'])
        
        if not user:
            api.abort(401, 'Invalid credentials')
        
        # Verify password
        if not user.verify_password(credentials['password']):
            api.abort(401, 'Invalid credentials')
        
        # Create JWT token with additional claims
        additional_claims = {
            'is_admin': user.is_admin,
            'email': user.email
        }
        
        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims
        )
        
        return {
            'access_token': access_token,
            'user': user.to_dict()
        }, 200

@api.route('/protected')
class Protected(Resource):
    @api.doc('protected_endpoint', security='Bearer')
    @jwt_required()
    def get(self):
        """
        Example protected endpoint
        Requires valid JWT token
        """
        current_user_id = get_jwt_identity()
        user = facade.get_user(current_user_id)
        
        if not user:
            api.abort(404, 'User not found')
        
        return {
            'message': f'Hello, {user.first_name}!',
            'user_id': current_user_id
        }, 200