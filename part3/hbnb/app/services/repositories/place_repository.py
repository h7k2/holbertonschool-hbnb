from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """Repository for Place-specific database operations"""
    
    def __init__(self):
        """Initialize PlaceRepository with Place model"""
        super().__init__(Place)

    def get_all_places(self):
        """Get all places from the database"""
        return self.get_all()