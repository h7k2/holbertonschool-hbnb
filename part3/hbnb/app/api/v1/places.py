from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# Modèle pour la création de place
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(required=True, description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.doc(security='Bearer')
    @jwt_required()
    def post(self):
        """Create a new place"""
        current_user_id = get_jwt_identity()
        place_data = api.payload
        place_data['owner_id'] = current_user_id
        
        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('list_places')
    def get(self):
        """Get all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

@api.route('/<place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.doc('get_place')
    def get(self, place_id):
        """Get place by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        return place.to_dict(), 200

    @api.doc(security='Bearer')
    @jwt_required()
    def put(self, place_id):
        """Update a place"""
        place_data = api.payload
        updated_place = facade.update_place(place_id, place_data)
        if not updated_place:
            api.abort(404, 'Place not found')
        return updated_place.to_dict(), 200

    @api.doc(security='Bearer')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        success = facade.delete_place(place_id)
        if not success:
            api.abort(404, 'Place not found')
        return {'message': 'Place deleted'}, 200

@api.route('/<place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviews(Resource):
    @api.doc('get_place_reviews')
    def get(self, place_id):
        """Get all reviews for a place"""
        reviews = facade.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews], 200

@api.route('/<place_id>/amenities')
@api.param('place_id', 'The place identifier')
class PlaceAmenities(Resource):
    @api.doc('get_place_amenities')
    def get(self, place_id):
        """Get all amenities for a place"""
        amenities = facade.get_place_amenities(place_id)
        return [amenity.to_dict() for amenity in amenities], 200
    
    @api.doc(security='Bearer')
    @jwt_required()
    def post(self, place_id):
        """Add amenity to place"""
        data = api.payload
        amenity_id = data.get('amenity_id')
        
        if not amenity_id:
            api.abort(400, 'amenity_id is required')
        
        success = facade.add_amenity_to_place(place_id, amenity_id)
        if success:
            return {'message': 'Amenity added to place'}, 201
        api.abort(400, 'Failed to add amenity')