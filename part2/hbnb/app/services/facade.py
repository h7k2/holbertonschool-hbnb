from typing import Any, Dict, List, Optional
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(
        self,
        user_repo: Optional[InMemoryRepository] = None,
        place_repo: Optional[InMemoryRepository] = None,
        review_repo: Optional[InMemoryRepository] = None,
        amenity_repo: Optional[InMemoryRepository] = None,
    ) -> None:
        self.user_repo = user_repo or InMemoryRepository()
        self.place_repo = place_repo or InMemoryRepository()
        self.review_repo = review_repo or InMemoryRepository()
        self.amenity_repo = amenity_repo or InMemoryRepository()

# user
    def create_user(self, user_data: Dict[str, Any]) -> Any:
        raise NotImplementedError

    def get_user(self, user_id: str) -> Optional[Any]:
        raise NotImplementedError

    def list_users(self) -> List[Any]:
        raise NotImplementedError

    def update_user(self, user_id: str, patch: Dict[str, Any]) -> Optional[Any]:
        raise NotImplementedError

# amenity
    def create_amenity(self, amenity_data: Dict[str, Any]) -> Any:
        raise NotImplementedError

    def get_amenity(self, amenity_id: str) -> Optional[Any]:
        raise NotImplementedError

    def list_amenities(self) -> List[Any]:
        raise NotImplementedError

    def update_amenity(self, amenity_id: str, patch: Dict[str, Any]) -> Optional[Any]:
        raise NotImplementedError
    
# place
    def create_place(self, place_data: Dict[str, Any]) -> Any:
        raise NotImplementedError

    def get_place(self, place_id: str) -> Optional[Any]:
        raise NotImplementedError

    def list_places(self) -> List[Any]:
        raise NotImplementedError

    def update_place(self, place_id: str, patch: Dict[str, Any]) -> Optional[Any]:
        raise NotImplementedError

#review   
def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
    pass

def get_review(self, review_id):
    # Placeholder for logic to retrieve a review by ID
    pass

def get_all_reviews(self):
    # Placeholder for logic to retrieve all reviews
    pass

def get_reviews_by_place(self, place_id):
    # Placeholder for logic to retrieve all reviews for a specific place
    pass

def update_review(self, review_id, review_data):
    # Placeholder for logic to update a review
    pass

def delete_review(self, review_id):
    # Placeholder for logic to delete a review
    pass

# serialization
    def place_with_related(self, place_id: str) -> Dict[str, Any]:
        raise NotImplementedError
