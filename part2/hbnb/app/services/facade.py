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
    def create_review(self, review_data: Dict[str, Any]) -> Any:
        raise NotImplementedError

    def get_review(self, review_id: str) -> Optional[Any]:
        raise NotImplementedError

    def list_reviews(self, place_id: Optional[str] = None) -> List[Any]:
        raise NotImplementedError

    def update_review(self, review_id: str, patch: Dict[str, Any]) -> Optional[Any]:
        raise NotImplementedError

    def delete_review(self, review_id: str) -> None:
        raise NotImplementedError

# serialization
    def place_with_related(self, place_id: str) -> Dict[str, Any]:
        raise NotImplementedError
