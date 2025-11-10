from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories import UserRepository, PlaceRepository, ReviewRepository, AmenityRepository
from typing import Dict, Any, Optional, List


class HBnBFacade:
    """
    Facade class to handle business logic for HBnB application
    """
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ========== USER METHODS ==========
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        # Vérifier si l'email existe déjà
        existing_user = self.user_repo.get_by_attribute('email', user_data['email'])
        if existing_user:
            raise ValueError("Email already registered")
        
        # Créer l'utilisateur
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=user_data.get('is_admin', False)
        )
        
        # Hash le password AVANT de sauvegarder
        user.hash_password(user_data['password'])
        
        # Ajouter et retourner l'utilisateur créé
        self.user_repo.add(user)
        return user  # ← Retourner l'objet user au lieu du résultat de add()

    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email address"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self) -> List[User]:
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Optional[User]:
        """Update a user"""
        user = self.get_user(user_id)
        if not user:
            return None
        
        # Update only allowed fields
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            # Check if email is already taken
            existing = self.get_user_by_email(user_data['email'])
            if existing and existing.id != user_id:
                raise ValueError('Email already registered')
            user.email = user_data['email']
        if 'password' in user_data:
            user.hash_password(user_data['password'])
        
        return user

    def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        return self.user_repo.delete(user_id)

    # ========== PLACE METHODS ==========
    def place_with_related(self, place_id: str) -> Dict[str, Any]:
        """Get place with related data"""
        place = self.get_place(place_id)
        if not place:
            return None
        
        place_dict = place.to_dict()
        # Add related data if needed
        return place_dict

    def create_place(self, place_data):
        """Create a new place"""
        # Adapter selon les noms d'attributs de ton modèle Place
        place = Place(
            title=place_data['name'],  # name -> title
            description=place_data['description'],
            price=place_data['price_by_night'],  # price_by_night -> price
            latitude=place_data.get('latitude', 0.0),  # valeur par défaut
            longitude=place_data.get('longitude', 0.0),  # valeur par défaut
            owner_id=place_data.get('user_id')  # user_id -> owner_id
        )
        
        self.place_repo.add(place)
        return place  # ← Correction ici aussi

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def get_place(self, place_id):
        """Get a place by ID"""
        return self.place_repo.get(place_id)

    def update_place(self, place_id, place_data):
        """Update a place"""
        return self.place_repo.update(place_id, place_data)

    def delete_place(self, place_id):
        """Delete a place"""
        return self.place_repo.delete(place_id)

    # ========== REVIEW METHODS ==========
    def create_review(self, review_data):
        """Create a new review"""
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=review_data['place_id'],
            user_id=review_data['user_id']
        )
        
        self.review_repo.add(review)
        return review  # ← Et ici

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_user(self, user_id: str) -> List[Review]:
        """Get all reviews by a user"""
        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.user_id == user_id]

    def get_reviews_by_place(self, place_id: str) -> List[Review]:
        """Get all reviews for a place"""
        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.place_id == place_id]

    def get_review(self, review_id):
        """Get a review by ID"""
        return self.review_repo.get(review_id)

    def update_review(self, review_id, review_data):
        """Update a review"""
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review"""
        return self.review_repo.delete(review_id)

    # ========== AMENITY METHODS ==========
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(name=amenity_data['name'])  # ← Passer le name en argument
        
        self.amenity_repo.add(amenity)
        return amenity

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def get_amenity(self, amenity_id):
        """Get an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        return self.amenity_repo.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        """Delete an amenity"""
        return self.amenity_repo.delete(amenity_id)

    # ========== ADDITIONAL METHODS ==========
    def get_places_by_owner(self, user_id: str):
        """Get all places owned by a user"""
        places = self.place_repo.get_all()
        return [place for place in places if place.owner_id == user_id]

    def get_reviews_by_user(self, user_id: str):
        """Get all reviews by a user"""  
        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.user_id == user_id]

    def get_reviews_by_place(self, place_id: str):
        """Get all reviews for a place"""
        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.place_id == place_id]

    def get_place_amenities(self, place_id: str):
        """Get all amenities for a place"""
        place = self.place_repo.get(place_id)
        if place and hasattr(place, 'amenities'):
            return place.amenities
        return []

    def get_places_by_amenity(self, amenity_id: str):
        """Get all places that have this amenity"""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity and hasattr(amenity, 'places'):
            return amenity.places
        return []

    def add_amenity_to_place(self, place_id: str, amenity_id: str) -> bool:
        """Add an amenity to a place (Many-to-Many)"""
        try:
            place = self.place_repo.get(place_id)
            amenity = self.amenity_repo.get(amenity_id)
            
            if place and amenity:
                # Vérifier si la relation existe déjà
                if hasattr(place, 'amenities') and amenity not in place.amenities:
                    place.amenities.append(amenity)
                    # Force save
                    from app.extensions import db
                    db.session.commit()
                    return True
            return False
        except Exception as e:
            print(f"Error adding amenity to place: {e}")
            return False
