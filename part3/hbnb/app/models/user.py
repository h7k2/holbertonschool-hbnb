from app.extensions import db, bcrypt
from app.models.base import BaseModel
from sqlalchemy.orm import validates


class User(BaseModel):
    """User model for storing user information"""
    
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """Initialize a User instance"""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)

    def hash_password(self, password):
        """Hash the password before storing it"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password"""
        return bcrypt.check_password_hash(self.password_hash, password)

    @validates('email')
    def validate_email(self, key, email):
        """Validate email format"""
        if not email or '@' not in email:
            raise ValueError("Invalid email format")
        return email.lower()

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        """Validate name fields are not empty"""
        if not value or not value.strip():
            raise ValueError(f"{key} cannot be empty")
        if len(value) > 50:
            raise ValueError(f"{key} cannot exceed 50 characters")
        return value.strip()

    def to_dict(self):
        """Convert User instance to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        """String representation of User"""
        return f"<User {self.email}>"