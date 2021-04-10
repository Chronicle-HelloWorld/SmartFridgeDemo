from math import isclose
from typing import Optional

import database_funcs as db
from utils import try_parse_float


class Item:
    name: str
    brand: str
    category: str
    __qty: float

    def __init__(self, name: str):
        self.name = name
        self.__qty = 0
        self.brand = ""
        self.category = ""

    @property
    def qty(self):
        return self.__qty

    @qty.setter
    def qty(self, value: float):
        self.__qty = max(value, 0)

    def __repr__(self):
        return f"{self.name} - {self.qty:.2f}{f', brand: {self.brand}' if self.brand else ''}{f', category: {self.category}' if self.category else ''}"


class InventoryManager:
    inventory: dict[str, Item]

    def __init__(self):
        self.inventory = {}

    def update_item(self, args: list[str]) -> Optional[Item]:
        if len(args) < 2:
            return None

        name = args[0]
        result = try_parse_float(args[1])

        if not result[0]:
            return None

        qty = result[1]
        brand = ""
        category = ""

        if len(args) > 2:
            brand = args[2]

        if len(args) > 3:
            category = args[3]

        key = InventoryManager.__item_key__(name)

        if not (item := self.inventory.get(key)):
            item = Item(name)
            self.inventory[key] = item
            item.brand = brand
            item.category = category

        item.qty += qty
        db.add_item(item.name, item.brand, item.category, qty)

        if isclose(item.qty, 0):
            self.remove_item(item.name)

        return item

    def remove_item(self, name: str) -> Optional[Item]:
        key = InventoryManager.__item_key__(name)
        item = self.inventory.pop(key, None)

        if item is not None:
            db.remove_item(item.name, item.brand)

        return item

    def refresh_inventory(self):
        self.inventory.clear()

        for db_item in db.get_all_items():
            name = db_item[0]
            brand = db_item[1]
            category = db_item[2]
            qty = db_item[3]
            item = Item(name)
            item.qty = qty
            item.brand = brand
            item.category = category
            self.inventory[InventoryManager.__item_key__(item.name)] = item

    def list_inventory(self) -> list[str]:
        return [str(item) for item in self.inventory.values()]

    @staticmethod
    def __item_key__(name: str) -> str:
        return name.lower()
