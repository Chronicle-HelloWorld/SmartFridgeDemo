from math import isclose
from typing import Optional

import database_funcs as db
import csv
from order_manager import *


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

    def list_low_inventory(self) -> list[str]:
        # return a list of str representation of items (similar to list_inventory),
        # with quantity below the values in self.low_threshold
        # may also give the low threshold for each item
        output = []
        for item in self.inventory:
            if item[1] < self.low_threshold[item[0]]:
                output.append(item[0])
        return output

    def refill_low_inventory(self):
        # for each of the items currently has low inventory,
        # place an order with appropriate qty by calling the self.order_manager.cart_add_from_best
        pass

    @staticmethod
    def __item_key__(name: str) -> str:
        return name.lower()

    def __load_low_inv_thresholds(self):
        # read a file for low inventory threshold for items
        # place into self.low_threshold
        pass
        with open('low_inventory_thresholds.csv') as file:
            rows = csv.reader(file)
            for row in rows:
                self.low_threshold[row[0]] = row[1]
