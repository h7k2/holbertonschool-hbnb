from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Repository for User-specific database operations"""
    
    def __init__(self):
        """Initialize UserRepository with User model"""
        super().__init__(User)

    def get_user_by_email(self, email):
        """
        Get a user by email address
        
        Args:
            email: The email address to search for
            
        Returns:
            User object if found, None otherwise
        """
        return self.model.query.filter_by(email=email.lower()).first()

    def get_all_users(self):
        """Get all users from the database"""
        return self.get_all()

    def user_exists(self, email):
        """
        Check if a user with the given email exists
        
        Args:
            email: The email address to check
            
        Returns:
            True if user exists, False otherwise
        """
        return self.get_user_by_email(email) is not None