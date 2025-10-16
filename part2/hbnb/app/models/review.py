from app.models.base_model import BaseModel

class Review(BaseModel):
    _reviews = []

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place_id = place_id
        self.user_id = user_id
        Review._reviews.append(self)

    @staticmethod
    def validate_text(text):
        """Validate review text"""
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")
        if not text.strip():
            raise ValueError("Review text cannot be empty")
        return text.strip()

    @staticmethod
    def validate_rating(rating):
        """Validate rating (must be between 1 and 5)"""
        if not isinstance(rating, (int, float)):
            raise ValueError("Rating must be a number")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return int(rating)

    @staticmethod
    def all():
        return Review._reviews

    def to_dict(self):
        """Convert review object to dictionary"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }