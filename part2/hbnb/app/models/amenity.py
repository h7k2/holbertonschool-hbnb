from .base_model import BaseModel

class Amenity(BaseModel):
    _amenities = []

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.validate()
        Amenity._amenities.append(self)

    def validate(self):
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Name must be a non-empty string")
        if len(self.name) > 50:
            raise ValueError("Name must be 50 characters or less")

    @staticmethod
    def all():
        return Amenity._amenities