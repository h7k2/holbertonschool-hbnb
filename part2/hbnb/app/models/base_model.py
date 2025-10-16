import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, data):
        """Update instance attributes from dictionary"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Convert instance to dictionary"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }