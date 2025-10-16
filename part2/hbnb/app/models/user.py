from app.models.base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.is_admin = is_admin

    @staticmethod
    def validate_name(name, field_name):
        """Validate name fields"""
        if not name or not isinstance(name, str):
            raise ValueError(f"{field_name} is required and must be a string")
        if len(name) > 50:
            raise ValueError(f"{field_name} must not exceed 50 characters")
        if not name.strip():
            raise ValueError(f"{field_name} cannot be empty or whitespace only")
        return name.strip()

    @staticmethod
    def validate_email(email):
        """Validate email format and requirements"""
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        # Basic email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        
        return email.lower().strip()

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }