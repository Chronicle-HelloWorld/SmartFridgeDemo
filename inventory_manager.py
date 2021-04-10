from math import isclose
from typing import Optional

import database_funcs as db
from utils import try_parse_float
from item import *

class InventoryManager:
    inventory: dict[str, Item]

    def __init__(self):
        self.inventory = {}


    def update_item(self, name: str, qty: float, brand: str, category: str) -> Item:
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
