from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, min=1, max=5, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID')
})

@api.route('/', strict_slashes=False)
class ReviewList(Resource):

        def options(self):
            return {}, 200

        @api.expect(review_model)
        @jwt_required()
        def post(self):
            """Create a new review"""
            claims = get_jwt()
            current_user_id = get_jwt_identity()
            review_data = request.get_json()
            review_data['user_id'] = current_user_id

            # Règle métier : ne pas reviewer son propre place
            place = facade.get_place(review_data['place_id'])
            if place and place.owner_id == current_user_id and not claims.get('is_admin', False):
                return {'message': "You can't review your own place"}, 403

            # Règle métier : ne pas reviewer deux fois le même place
            if facade.has_user_reviewed_place(current_user_id, review_data['place_id']) and not claims.get('is_admin', False):
                return {'message': "You can't review the same place twice"}, 403

            try:
                new_review = facade.create_review(review_data)
                return new_review.to_dict(), 201
            except Exception as e:
                return {'message': str(e)}, 400

        def get(self):
            """Get all reviews"""
            reviews = facade.get_all_reviews()
            return [review.to_dict() for review in reviews], 200

@api.route('/<review_id>', strict_slashes=False)
class ReviewResource(Resource):
        def options(self, review_id):
            return {}, 200
        def get(self, review_id):
            """Get a specific review"""
            review = facade.get_review(review_id)
            if not review:
                return {'message': 'Review not found'}, 404
            return review.to_dict(), 200

        @jwt_required()
        def put(self, review_id):
            """Update a review (author or admin only)"""
            claims = get_jwt()
            current_user_id = get_jwt_identity()
            review = facade.get_review(review_id)
            if not review:
                return {'message': 'Review not found'}, 404
            # Contrôle d'ownership ou admin
            if not claims.get('is_admin', False) and review.user_id != current_user_id:
                return {'message': 'Unauthorized action'}, 403
            review_data = request.get_json()
            updated_review = facade.update_review(review_id, review_data)
            return updated_review.to_dict(), 200

        @jwt_required()
        def delete(self, review_id):
            """Delete a review (author or admin only)"""
            claims = get_jwt()
            current_user_id = get_jwt_identity()
            review = facade.get_review(review_id)
            if not review:
                return {'message': 'Review not found'}, 404
            # Contrôle d'ownership ou admin
            if not claims.get('is_admin', False) and review.user_id != current_user_id:
                return {'message': 'Unauthorized action'}, 403
            success = facade.delete_review(review_id)
            if not success:
                return {'message': 'Review not found'}, 404
            return '', 204