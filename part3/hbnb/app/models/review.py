from app.extensions import db
from app.models.base import BaseModel
from sqlalchemy.orm import validates


class Review(BaseModel):
    """Review model for storing review information"""

    __tablename__ = 'reviews'

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), nullable=False)  # Temporaire, relation ajoutée plus tard
    user_id = db.Column(db.String(36), nullable=False)   # Temporaire, relation ajoutée plus tard

    # Ces attributs seront ajoutés plus tard avec les relations
    # place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    # user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place_id, user_id):
        """Initialize a Review instance"""
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @validates('text')
    def validate_text(self, key, text):
        """Validate text is not empty"""
        if not text or not text.strip():
            raise ValueError("Review text cannot be empty")
        if len(text) > 500:
            raise ValueError("Review text cannot exceed 500 characters")
        return text.strip()

    @validates('rating')
    def validate_rating(self, key, rating):
        """Validate rating is between 1 and 5"""
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating

    def to_dict(self):
        """Convert Review instance to dictionary"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        """String representation of Review"""
        return f"<Review {self.id} - Rating: {self.rating}>"