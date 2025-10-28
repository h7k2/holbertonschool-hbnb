from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository
from typing import Dict, Any, Optional, List

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ========== USER METHODS ==========
    def create_user(self, user_data: Dict[str, Any]) -> Any:
        """Create a new user"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user_by_email(self, email: str) -> Optional[Any]:
        """Get a user by email address"""
        users = self.user_repo.get_all()
        for user in users:
            if user.email == email:
                return user
        return None

    def get_user(self, user_id: str) -> Optional[Any]:
        """Get a user by ID"""
        return self.user_repo.get(user_id)

    def get_all_users(self) -> List[Any]:
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Optional[Any]:
        """Update a user"""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        
        # Update only allowed fields
        if 'first_name' in user_data:
            user.first_name = user.validate_name(user_data['first_name'], "First name")
        if 'last_name' in user_data:
            user.last_name = user.validate_name(user_data['last_name'], "Last name")
        if 'email' in user_data:
            # Check if new email is already used by another user
            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")
            user.email = user.validate_email(user_data['email'])
        
        # Update timestamp
        user.update_timestamp()
        
        # Save back to repository
        self.user_repo._storage[user_id] = user
        
        return user

    def delete_review(self, review_id: str) -> bool:
        """Delete a review"""
        return self.review_repo.delete(review_id)

    # serialization
    def place_with_related(self, place_id: str) -> Dict[str, Any]:
        raise NotImplementedError

    def create_place(self, place_data):
        """
        Crée un nouveau lieu (place) avec les données fournies.
        """
        from app.models.place import Place  # <-- adaptez ce chemin selon l'emplacement réel
        new_place = Place(**place_data)
        new_place.save()
        return new_place

    def get_all_places(self):
        """
        Retourne la liste de tous les lieux (places).
        """
        from app.models.place import Place  # adapte le chemin si besoin
        # Supposons que tu as une variable de classe ou globale qui stocke les places
        return Place.all()  # ou Place.objects(), ou Place.storage, selon ton implémentation

    def get_place(self, place_id):
        """
        Retourne un lieu (place) selon son identifiant.
        """
        from app.models.place import Place  # adapte le chemin si besoin
        # Exemple si tu as une méthode statique all() qui retourne toutes les places
        for place in Place.all():
            if getattr(place, "id", None) == place_id:
                return place
        return None

    def update_place(self, place_id, place_data):
        """
        Met à jour un lieu (place) avec les nouvelles données.
        """
        from app.models.place import Place  # adapte le chemin si besoin
        place = self.get_place(place_id)
        if not place:
            return None
        for key, value in place_data.items():
            setattr(place, key, value)
        if hasattr(place, "save"):
            place.save()
        return place

    def create_review(self, review_data):
        """
        Crée un nouvel avis (review) avec les données fournies.
        """
        from app.models.review import Review  # adapte le chemin si besoin
        new_review = Review(**review_data)
        if hasattr(new_review, "save"):
            new_review.save()
        return new_review

    def get_all_reviews(self):
        """
        Retourne la liste de tous les avis (reviews).
        """
        from app.models.review import Review
        return Review.all()

    def get_reviews_by_place(self, place_id):
        """
        Retourne la liste des avis (reviews) pour un lieu (place) donné.
        """
        from app.models.review import Review  # adapte le chemin si besoin
        return [review for review in Review.all() if getattr(review, "place_id", None) == place_id]

    def get_review(self, review_id):
        """
        Retourne un avis (review) selon son identifiant.
        """
        from app.models.review import Review  # adapte le chemin si besoin
        for review in Review.all():
            if getattr(review, "id", None) == review_id:
                return review
        return None

    def create_amenity(self, amenity_data):
        """
        Crée une nouvelle commodité (amenity) avec les données fournies.
        """
        from app.models.amenity import Amenity  # adapte le chemin si besoin
        new_amenity = Amenity(**amenity_data)
        if hasattr(new_amenity, "save"):
            new_amenity.save()
        return new_amenity

    def get_all_amenities(self):
        """
        Retourne la liste de toutes les commodités (amenities).
        """
        from app.models.amenity import Amenity  # adapte le chemin si besoin
        return Amenity.all()  # ou la méthode adaptée à ton stockage

    def get_amenity(self, amenity_id):
        """
        Retourne une commodité (amenity) selon son identifiant.
        """
        from app.models.amenity import Amenity  # adapte le chemin si besoin
        for amenity in Amenity.all():
            if getattr(amenity, "id", None) == amenity_id:
                return amenity
        return None

    def update_amenity(self, amenity_id, amenity_data):
        """
        Met à jour une commodité (amenity) avec les nouvelles données.
        """
        from app.models.amenity import Amenity  # adapte le chemin si besoin
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        if hasattr(amenity, "save"):
            amenity.save()
        return amenity

    def update_review(self, review_id, review_data):
        """
        Met à jour un avis (review) avec les nouvelles données.
        """
        from app.models.review import Review  # adapte le chemin si besoin
        review = self.get_review(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            setattr(review, key, value)
        if hasattr(review, "save"):
            review.save()
        return review

    def delete_place(self, place_id):
        """
        Supprime un lieu (place) selon son identifiant.
        """
        from app.models.place import Place  # adapte le chemin si besoin
        place = self.get_place(place_id)
        if not place:
            return False
        if hasattr(Place, "_places"):
            Place._places.remove(place)
        elif hasattr(place, "delete"):
            place.delete()
        return True

    def delete_user(self, user_id):
        """
        Supprime un utilisateur selon son identifiant.
        """
        from app.models.user import User  # adapte le chemin si besoin
        user = self.get_user(user_id)
        if not user:
            return False
        if hasattr(User, "_users"):
            User._users.remove(user)
        elif hasattr(user, "delete"):
            user.delete()
        return True
