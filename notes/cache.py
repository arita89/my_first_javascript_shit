# cache.py
from typing import List, Dict

class ErrorCache:
    _instance = None

    def __init__(self):
        self.errors: List[Dict] = []

    def add_error(self, error: Dict):
        """Add an error to the cache."""
        self.errors.append(error)

    def get_sorted_errors(self, sort_key: str) -> List[Dict]:
        """Retrieve errors sorted by a specified key."""
        return sorted(self.errors, key=lambda x: x.get(sort_key, ""))

    @classmethod
    def get_instance(cls):
        """Singleton access method to get the instance of ErrorCache."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
