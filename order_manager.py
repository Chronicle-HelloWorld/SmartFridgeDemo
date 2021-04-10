from collections import defaultdict

from api_supermarkets import *
from item import *


class Order:
    item: Item
    unit_price: float
    vendor: Supermarket

    def __init__(self, item: Item, unit_price: float, vendor: Supermarket):
        self.item = item
        self.unit_price = unit_price
        self.vendor = vendor

    @property
    def price(self) -> float:
        return self.item.qty * self.unit_price


class OrderManager:
    vendors: dict[str, Supermarket]
    cart: dict[str, dict[str, Order]]

    def __init__(self, vendors: list[Supermarket]):
        self.vendors = dict((vendor.name, vendor) for vendor in vendors)
        self.cart = defaultdict(dict[str, Order])

    def cart_add_from_best(self, name: str, qty: float):
        best_price, best_vendor = min((vendor.query_price(name), vendor) for vendor in self.vendors.values())
        self.__cart_add(name, qty, best_vendor, best_price)

    def cart_add_from_vendor(self, name: str, qty: float, vendor_name: str):
        if (vendor := self.vendors.get(vendor_name)) is None:
            return

        self.__cart_add(name, qty, vendor)

    def __cart_add(self, name: str, qty: float, vendor: Supermarket, price: float = None):
        vendor_orders = self.cart[name]

        if (order := vendor_orders.get(vendor.name, None)) is None:
            item = Item(name)

            if price is None:
                price = vendor.query_price(name)

            order = Order(item, price, vendor)
            vendor_orders[vendor.name] = order

        order.item.qty += qty

    def cart_remove(self, name: str = None, vendor: str = None, qty: float = None):
        if name is None:
            self.cart.clear()
            return

        if (vendor_orders := self.cart.get(name, None)) is None:
            return

        if vendor is None:
            vendor_orders.clear()
            return

        if qty is None:
            vendor_orders.pop(vendor)
        elif (order := vendor_orders.get(vendor, None)) is not None:
            order.item.qty -= qty

    def cart_checkout(self):
        orders = defaultdict(dict[str, Order])

        for item, vendor_orders in self.cart.items():
            for vendor, order in vendor_orders.items():
                orders[vendor][item] = order

        for vendor, vendor_orders in orders.items():
            self.vendors[vendor].place_order(dict((o.item.name, o.item.qty) for o in vendor_orders.values()))

        self.cart.clear()

    def view_cart(self) -> str:
        header = f"{'Product':<20}{'Quantity':>10}{'Unit Price':>15}{'Price':>10}{'Vendor':>20}"
        lines = [header]
        total = 0

        for item, vendor_orders in self.cart.items():
            for order in vendor_orders.values():
                lines.append(
                    f"{order.item.name:<20}{order.item.qty:>10.2f}{order.unit_price:>15.2f}{order.price:>10.2f}{order.vendor.name:>20}")
                total += order.price

        lines.append(f"{'Total':<20}{'':>10}{'':>15}{total:>10.2f}")
        return "\n".join(lines)
