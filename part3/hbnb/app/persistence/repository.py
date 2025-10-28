from abc import ABC, abstractmethod

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
        """Update an object - data can be dict or object"""
        obj = self.get(obj_id)
        if obj:
            # Si data a un attribut 'id', c'est un objet, on le remplace
            if hasattr(data, 'id'):
                self._storage[obj_id] = data
                if hasattr(data, 'update_timestamp'):
                    data.update_timestamp()
            # Sinon c'est un dict, on met à jour les attributs
            elif isinstance(data, dict):
                if hasattr(obj, 'update'):
                    obj.update(data)
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
