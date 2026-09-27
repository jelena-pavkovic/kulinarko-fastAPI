from abc import ABC, abstractmethod

class Item(ABC):
    @abstractmethod
    def get_data(self) -> dict:
        pass

class IngredientItem(Item):
    def __init__(self, item_id: int, name: str, default_unit: str):
        self.item_id = item_id
        self.name = name
        self.default_unit = default_unit

    def get_data(self) -> dict:
        return {"id": self.item_id, "name": self.name, "default_unit": self.default_unit}

class ItemFactory(ABC):
    @abstractmethod
    def get_or_create(self, name: str, default_unit: str = None) -> Item:
        pass

class IngredientFactory(ItemFactory):
    def __init__(self, db_adapter):
        self.db_adapter = db_adapter 

    def get_or_create(self, name: str, default_unit: str = None) -> IngredientItem:
        existing = self.db_adapter.find_by_name(name)
        if existing:
            return IngredientItem(existing["id"], existing["name"], existing["default_unit"])
        
        new_data = self.db_adapter.save_ingredient(name, default_unit)
        return IngredientItem(new_data["id"], new_data["name"], new_data["default_unit"])


"""

from .ingredient_repository import IngredientRepository

class IngredientFactory:
    def __init__(self, repository: IngredientRepository):
        self.repository = repository

    def get_or_create(self, name: str, default_unit: str = None):
        existing = self.repository.find_by_name(name)
        if existing:
            return existing
        return self.repository.save(name, default_unit)
"""