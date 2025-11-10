from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade  # Import direct

api = Namespace('places', description='Place operations')
facade = HBnBFacade()  # Instance locale

# Modèle correct avec les bons noms de champs
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(required=True, description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @jwt_required()
    def post(self):
        """Create a new place"""
        current_user_id = get_jwt_identity()
        place_data = request.get_json()
        
        # CORRECTION CRITIQUE : Ajouter l'owner_id
        place_data['owner_id'] = current_user_id
        
        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except Exception as e:
            return {'message': str(e)}, 400

    def get(self):
        """Get all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Get place by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

@api.route('/<place_id>/reviews/')
class PlaceReviews(Resource):
    def get(self, place_id):
        """Get all reviews for a place"""
        reviews = facade.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews], 200

@api.route('/<place_id>/amenities/')
class PlaceAmenities(Resource):
    def get(self, place_id):
        """Get all amenities for a place"""
        amenities = facade.get_place_amenities(place_id)
        return [amenity.to_dict() for amenity in amenities], 200
    
    @jwt_required()
    def post(self, place_id):
        """Add amenity to place"""
        data = request.get_json()
        amenity_id = data.get('amenity_id')
        
        # DEBUG temporaire
        print(f"🔍 Place ID: {place_id}")
        print(f"🔍 Amenity ID: {amenity_id}")
        print(f"🔍 Data reçue: {data}")
        
        success = facade.add_amenity_to_place(place_id, amenity_id)
        print(f"🔍 Résultat facade: {success}")
        
        if success:
            return {'message': 'Amenity added to place'}, 201
        return {'message': 'Failed to add amenity'}, 400