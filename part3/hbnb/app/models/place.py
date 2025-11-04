from app.extensions import db
from app.models.base import BaseModel
from sqlalchemy.orm import validates


class Place(BaseModel):
    """Place model for storing place information"""

    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)  # Temporaire, relation ajoutée plus tard

    # Ces attributs seront ajoutés plus tard avec les relations
    # amenities = relationship...
    # reviews = relationship...

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """Initialize a Place instance"""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

    @validates('title')
    def validate_title(self, key, title):
        """Validate title is not empty and within length limits"""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        return title.strip()

    @validates('price')
    def validate_price(self, key, price):
        """Validate price is positive"""
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        return price

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        """Validate latitude is within valid range"""
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return latitude

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        """Validate longitude is within valid range"""
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return longitude

    def to_dict(self):
        """Convert Place instance to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        """String representation of Place"""
        return f"<Place {self.title}>"