from math import isclose
from typing import Optional

import database_funcs as db
import csv
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
        output = [f"{'Name':<20}{'Current Qty':>15}{'Threshold':>15}"]

        for item in self.inventory.values():
            current_quantity = item.qty
            threshold = self.low_threshold[key(item.name)]

            if current_quantity < threshold:
                output.append(f"{item.name:<20}{item.qty:>15.2f}{threshold:>15}")

        return output

    def refill_low_inventory(self):
        # for each of the items currently has low inventory,
        # place an order with appropriate qty by calling the self.order_manager.cart_add_from_best
        for item in self.inventory:
            current_quantity = self.inventory[item].qty
            threshold_qty = self.low_threshold[key(item)]
            if current_quantity < threshold_qty:
                order_qty = 4 * threshold_qty - current_quantity
                self.order_manager.cart_add_from_best(item, order_qty)

    def __load_low_inv_thresholds(self):
        # read a file for low inventory threshold for items
        # place into self.low_threshold
        with open('low_inventory_thresholds.csv') as file:
            rows = csv.reader(file)
            for row in rows:
                self.low_threshold[key(row[0])] = float(row[1])
