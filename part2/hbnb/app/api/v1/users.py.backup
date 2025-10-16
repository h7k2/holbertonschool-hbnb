from flask_restx import Namespace, Resource, fields
from app.api.v1 import facade

api = Namespace('users', description='User operations')

# Model for creating a user (all fields required)
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address')
})

# Model for updating a user (all fields optional)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name'),
    'last_name': fields.String(required=False, description='Last name'),
    'email': fields.String(required=False, description='Email address')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input')
    def post(self):
        """Create a new user"""
        user_data = api.payload
        
        # Check if email already exists
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in users
        ], 200

@api.route('/<string:id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, id):
        """Get user details by ID"""
        user = facade.get_user(id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, id):
        """Update user details"""
        user_data = api.payload
        try:
            user = facade.update_user(id, user_data)
            if not user:
                return {'error': 'User not found'}, 404
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, id):
        """Delete a user"""
        if facade.delete_user(id):
            return {'message': 'User deleted successfully'}, 200
        return {'error': 'User not found'}, 404