from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    """Repository for Review-specific database operations"""
    
    def __init__(self):
        """Initialize ReviewRepository with Review model"""
        super().__init__(Review)

    def get_all_reviews(self):
        """Get all reviews from the database"""
        return self.get_all()