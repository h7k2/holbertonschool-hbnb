"""
Base model for all entities in the application
"""
import uuid
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    """
    Base model class that provides common attributes and methods for all models
    """
    __abstract__ = True  # This tells SQLAlchemy not to create a table for BaseModel
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Save the current instance to the database"""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete the current instance from the database"""
        db.session.delete(self)
        db.session.commit()
    
    def update(self, data):
        """Update the current instance with the provided data"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert the instance to a dictionary"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        """String representation of the instance"""
        return f"<{self.__class__.__name__} {self.id}>"