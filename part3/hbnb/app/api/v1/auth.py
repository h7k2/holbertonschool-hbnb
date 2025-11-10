from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from app.services.facade import HBnBFacade
from flask_jwt_extended import create_access_token

api = Namespace('auth', description='Authentication operations')
facade = HBnBFacade()

# Modèles pour la validation
user_registration = api.model('UserRegistration', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'), 
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

user_login = api.model('UserLogin', {
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

@api.route('/register')
class Register(Resource):
    @api.expect(user_registration)
    def post(self):
        """Register a new user"""
        try:
            data = request.get_json()
            user = facade.create_user(data)
            return user.to_dict(), 201
        except ValueError as e:
            return {'message': str(e)}, 400

@api.route('/login') 
class Login(Resource):
    @api.expect(user_login)
    def post(self):
        """User login"""
        try:
            data = request.get_json()
            user = facade.get_user_by_email(data['email'])
            
            if user and user.check_password(data['password']):  # ← Utiliser la méthode du modèle
                access_token = create_access_token(
                    identity=user.id,
                    additional_claims={
                        'email': user.email,
                        'is_admin': user.is_admin
                    }
                )
                return {
                    'access_token': access_token,
                    'user': user.to_dict()
                }, 200
            
            return {'message': 'Invalid credentials'}, 401
            
        except Exception as e:
            return {'message': str(e)}, 400