from math import isclose
from typing import Optional

import database_funcs as db
from order_manager import *
from utils import key


class InventoryManager:
    inventory: dict[str, Item]
    low_threshold: dict[str, float]
    order_manager: OrderManager

    def __init__(self, order_manager: OrderManager):
        self.inventory = {}
        self.low_threshold = defaultdict(float)
        self.order_manager = order_manager
        self.__load_low_inv_thresholds()

    def update_item(self, name: str, qty: float, brand: str, category: str) -> Item:
        namekey = key(name)

        if not (item := self.inventory.get(namekey)):
            item = Item(name)
            self.inventory[namekey] = item
            item.brand = brand
            item.category = category

        item.qty += qty
        db.add_item(item.name, item.brand, item.category, qty)

        if isclose(item.qty, 0):
            self.remove_item(item.name)

        return item

    def remove_item(self, name: str) -> Optional[Item]:
        item = self.inventory.pop(key(name), None)

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
            self.inventory[key(item.name)] = item

    def list_inventory(self) -> list[str]:
        return [str(item) for item in self.inventory.values()]

    def list_low_inventory(self) -> list[str]:
        # return a list of str representation of items (similar to list_inventory),
        # with quantity below the values in self.low_threshold
        # may also give the low threshold for each item
        pass

    def refill_low_inventory(self):
        # for each of the items currently has low inventory,
        # place an order with appropriate qty by calling the self.order_manager.cart_add_from_best
        pass

    def __load_low_inv_thresholds(self):
        # read a file for low inventory threshold for items
        # place into self.low_threshold
        pass
