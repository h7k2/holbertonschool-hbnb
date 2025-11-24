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
        """Create a new user (hash password before saving)"""
        user = User(**user_data)
        if 'password' in user_data:
            user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self) -> List[User]:
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Optional[User]:
        """Update user"""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        
        for key, value in user_data.items():
            if hasattr(user, key) and key not in ['id', 'created_at']:
                setattr(user, key, value)
        
        self.user_repo.update(user_id, user_data)
        return user

    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        user = self.user_repo.get(user_id)
        if not user:
            return False
        self.user_repo.delete(user_id)
        return True

    # ========== PLACE METHODS ==========
    def place_with_related(self, place_id: str) -> Dict[str, Any]:
        """Get place with related data (owner, amenities, reviews)"""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        place_dict = place.to_dict()
        place_dict['owner'] = place.owner.to_dict() if place.owner else None
        place_dict['amenities'] = [a.to_dict() for a in place.amenities]
        place_dict['reviews'] = [r.to_dict() for r in place.reviews]
        
        return place_dict

    def create_place(self, place_data: Dict[str, Any]) -> Place:
        """Create a new place"""
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError("Owner ID is required")
        
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_all_places(self) -> List[Place]:
        """Get all places"""
        return self.place_repo.get_all()

    def get_place(self, place_id: str) -> Optional[Place]:
        """Get place by ID"""
        return self.place_repo.get(place_id)

    def update_place(self, place_id: str, place_data: Dict[str, Any]) -> Optional[Place]:
        """Update place"""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        for key, value in place_data.items():
            if hasattr(place, key) and key not in ['id', 'created_at', 'owner_id']:
                setattr(place, key, value)
        
        self.place_repo.update(place_id, place_data)
        return place

    def delete_place(self, place_id: str) -> bool:
        """Delete place"""
        place = self.place_repo.get(place_id)
        if not place:
            return False
        self.place_repo.delete(place_id)
        return True

    def get_place_amenities(self, place_id: str) -> List[Amenity]:
        """Get all amenities for a place"""
        place = self.place_repo.get(place_id)
        if not place:
            return []
        return place.amenities

    def add_amenity_to_place(self, place_id: str, amenity_id: str) -> bool:
        """Add an amenity to a place"""
        place = self.place_repo.get(place_id)
        amenity = self.amenity_repo.get(amenity_id)
        
        if not place or not amenity:
            return False
        
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            self.place_repo.update(place_id, {})
        
        return True

    # ========== REVIEW METHODS ==========
    def create_review(self, review_data: Dict[str, Any]) -> Review:
        """Create a new review"""
        place_id = review_data.get('place_id')
        user_id = review_data.get('user_id')
        
        if not place_id or not user_id:
            raise ValueError("Place ID and User ID are required")
        
        place = self.place_repo.get(place_id)
        user = self.user_repo.get(user_id)
        
        if not place:
            raise ValueError("Place not found")
        if not user:
            raise ValueError("User not found")
        
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_all_reviews(self) -> List[Review]:
        """Get all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_user(self, user_id: str) -> List[Review]:
        """Get all reviews by a user"""
        return self.review_repo.get_by_attribute('user_id', user_id)

    def get_reviews_by_place(self, place_id: str) -> List[Review]:
        """Get all reviews for a place"""
        result = self.review_repo.get_by_attribute('place_id', place_id)
        if result is None:
            return []
        if isinstance(result, list):
            return result
        return [result]

    def get_review(self, review_id: str) -> Optional[Review]:
        """Get review by ID"""
        return self.review_repo.get(review_id)

    def update_review(self, review_id: str, review_data: Dict[str, Any]) -> Optional[Review]:
        """Update review"""
        review = self.review_repo.get(review_id)
        if not review:
            return None
        
        for key, value in review_data.items():
            if hasattr(review, key) and key not in ['id', 'created_at', 'user_id', 'place_id']:
                setattr(review, key, value)
        
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id: str) -> bool:
        """Delete review"""
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True

    # ========== AMENITY METHODS ==========
    def create_amenity(self, amenity_data: Dict[str, Any]) -> Amenity:
        """Create a new amenity"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_all_amenities(self) -> List[Amenity]:
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def update_amenity(self, amenity_id: str, amenity_data: Dict[str, Any]) -> Optional[Amenity]:
        """Update amenity"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        for key, value in amenity_data.items():
            if hasattr(amenity, key) and key not in ['id', 'created_at']:
                setattr(amenity, key, value)
        
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    def delete_amenity(self, amenity_id: str) -> bool:
        """Delete amenity"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False
        self.amenity_repo.delete(amenity_id)
        return True

    def has_user_reviewed_place(self, user_id: str, place_id: str) -> bool:
        """Return True if the user has already reviewed the place"""
        reviews = self.review_repo.get_all()
        for review in reviews:
            if review.user_id == user_id and review.place_id == place_id:
                return True
        return False
