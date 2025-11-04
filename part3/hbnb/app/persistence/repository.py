from abc import ABC, abstractmethod
from app.extensions import db

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    """In-memory repository for storing objects"""
    
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """Add an object to the repository"""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieve an object by ID"""
        return self._storage.get(obj_id)

    def get_all(self):
        """Retrieve all objects"""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object"""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key) and key not in ['id', 'created_at']:
                    setattr(obj, key, value)
            return obj
        return None

    def delete(self, obj_id):
        """Delete an object by ID"""
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by attribute value"""
        for obj in self._storage.values():
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None


class SQLAlchemyRepository(Repository):
    """SQLAlchemy-based repository for database persistence"""
    
    def __init__(self, model):
        """Initialize the repository with a SQLAlchemy model"""
        self.model = model
    
    def add(self, obj):
        """Add an object to the database"""
        db.session.add(obj)
        db.session.commit()
    
    def get(self, obj_id):
        """Get an object by ID"""
        return self.model.query.get(obj_id)
    
    def get_all(self):
        """Get all objects"""
        return self.model.query.all()
    
    def update(self, obj_id, data):
        """Update an object"""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key) and key not in ['id', 'created_at']:
                    setattr(obj, key, value)
            db.session.commit()
            return obj
        return None
    
    def delete(self, obj_id):
        """Delete an object"""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False
    
    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by a specific attribute"""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
