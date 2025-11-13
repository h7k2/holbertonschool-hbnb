from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')

# Define the user model for input validation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name', min_length=1, max_length=50),
    'last_name': fields.String(required=True, description='Last name', min_length=1, max_length=50),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password (min 8 characters)', min_length=8)
})

# Response model (without password)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

facade = HBnBFacade()

@api.route('/')
class UserList(Resource):
    @api.doc('list_users', security='Bearer')
    @api.marshal_list_with(user_response_model)
    @jwt_required()
    def get(self):
        """Retrieve all users (Protected)"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @api.doc('create_user', security='Bearer')
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    @jwt_required()  # ← Ajoute cette ligne !
    def post(self):
        """Register a new user (Admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, 'Admin privileges required')
        
        user_data = api.payload
        # Check if email exists
        if facade.get_user_by_email(user_data['email']):
            api.abort(409, 'Email already registered')
        
        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<user_id>')
class UserResource(Resource):
    @api.doc('get_user', security='Bearer')
    @api.marshal_with(user_response_model)
    @jwt_required()
    def get(self, user_id):
        """Get user by ID (Protected)"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user.to_dict(), 200

    @api.doc('update_user', security='Bearer')
    @api.expect(user_model)
    @api.marshal_with(user_response_model)
    @jwt_required()
    def put(self, user_id):
        """Update user (Protected - Owner or Admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Authorization check
        if current_user_id != user_id and not is_admin:
            api.abort(403, 'Unauthorized action')
        
        try:
            updated_user = facade.update_user(user_id, api.payload)
            if not updated_user:
                api.abort(404, 'User not found')
            return updated_user.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_user', security='Bearer')
    @jwt_required()
    def delete(self, user_id):
        """Delete user (Admin only)"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            api.abort(403, 'Admin privileges required')
        
        if not facade.delete_user(user_id):
            api.abort(404, 'User not found')
        return '', 204

@api.route('/<user_id>/places/')
class UserPlaces(Resource):
    @jwt_required()
    def get(self, user_id):
        """Get all places owned by a user"""
        places = facade.get_places_by_owner(user_id)
        return [place.to_dict() for place in places], 200

@api.route('/me/places')  
class MyPlaces(Resource):
    @jwt_required()
    def get(self):
        """Get current user's places"""
        current_user_id = get_jwt_identity()
        places = facade.get_places_by_owner(current_user_id)
        return [place.to_dict() for place in places], 200

@api.route('/<user_id>/reviews')
class UserReviews(Resource):
    @jwt_required()
    def get(self, user_id):
        """Get all reviews by a user"""
        reviews = facade.get_reviews_by_user(user_id)
        return [review.to_dict() for review in reviews], 200

@api.route('/me/reviews')
class MyReviews(Resource):
    @jwt_required()
    def get(self):
        """Get current user's reviews"""
        current_user_id = get_jwt_identity()
        reviews = facade.get_reviews_by_user(current_user_id)
        return [review.to_dict() for review in reviews], 200