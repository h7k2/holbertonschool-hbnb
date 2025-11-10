from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

# Model pour la validation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, min=1, max=5, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @jwt_required()
    def post(self):
        """Create a new review"""
        current_user_id = get_jwt_identity()
        review_data = request.get_json()
        
        # Ajouter l'user_id depuis le JWT
        review_data['user_id'] = current_user_id
        
        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except Exception as e:
            return {'message': str(e)}, 400

    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Get a specific review"""
        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        return review.to_dict(), 200

    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        review_data = request.get_json()
        review = facade.update_review(review_id, review_data)
        if not review:
            return {'message': 'Review not found'}, 404
        return review.to_dict(), 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        success = facade.delete_review(review_id)
        if not success:
            return {'message': 'Review not found'}, 404
        return '', 204