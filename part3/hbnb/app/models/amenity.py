from app.extensions import db
from app.models.base import BaseModel
from sqlalchemy.orm import validates

# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Amenity(BaseModel):
    """Amenity model for storing amenity information"""

    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    # Relationship
    places = db.relationship('Place', secondary=place_amenity, back_populates='amenities')

    def __init__(self, name):
        """Initialize an Amenity instance"""
        super().__init__()
        self.name = name

    @validates('name')
    def validate_name(self, key, name):
        """Validate name is not empty and within length limits"""
        if not name or not name.strip():
            raise ValueError("Amenity name cannot be empty")
        if len(name) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters")
        return name.strip()

    def to_dict(self):
        """Convert Amenity instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        """String representation of Amenity"""
        return f"<Amenity {self.name}>"