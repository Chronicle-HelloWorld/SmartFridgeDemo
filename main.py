import shlex

from inventory_manager import *
from order_manager import *
from recipes import *
from utils import *

is_running: bool
inv_manager: InventoryManager
order_manager: OrderManager
recipes: Recipes


def process_cmds(args: list[str]) -> bool:
    len_args = len(args)

    if len_args == 0:
        return False
    elif args[0] == "delorder":
        return process_delorder(args[1:])
    elif args[0] == "q":
        global is_running
        is_running = False
    elif args[0] == "list":
        for line in inv_manager.list_inventory():
            print(line)
    elif args[0] == "low":
        for line in inv_manager.list_low_inventory():
            print(line)
    elif args[0] == "refill":
        inv_manager.refill_low_inventory()
    elif args[0] == "cart":
        print(order_manager.view_cart())
    elif args[0] == "checkout":
        order_manager.cart_checkout()
    elif args[0] == "add":
        return process_add(args[1:])
    elif args[0] == "order":
        return process_order(args[1:])
    elif args[0] == "toprecipes":
        return process_top_recipes(args[1:])
    elif args[0] == "recipe":
        return process_recipe(args[1:])
    else:
        return False

    return True


def process_recipe(args: list[str]) -> bool:
    if len(args) == 0:
        return False

    for line in recipes.view_recipe(args[0], inv_manager.inventory):
        print(line)

    return True


def process_top_recipes(args: list[str]) -> bool:
    if len(args) == 0 or not (result := try_parse_int(args[0]))[0]:
        return False

    print(f"{'Name':<20}{'Match':>10}")

    for recipe, score in recipes.get_best_recipes(result[1], inv_manager.inventory).items():
        print(f"{recipe:<20}{score:>10.0f}")

    return True


def process_add(args: list[str]) -> bool:
    name = args[0]
    result = try_parse_float(args[1])

    if not result[0]:
        return False

    qty = result[1]
    brand = ""
    category = ""

    if len(args) > 2:
        brand = args[2]

    if len(args) > 3:
        category = args[3]

    item = inv_manager.update_item(name, qty, brand, category)
    print(item)
    return True


def process_order(args: list[str]) -> bool:
    name = args[0]
    result = try_parse_float(args[1])

    if not result[0]:
        return False

    qty = result[1]

    if len(args) > 2:
        vendor = args[2]
        order_manager.cart_add_from_vendor(name, qty, vendor)
    else:
        order_manager.cart_add_from_best(name, qty)

    return True


def process_delorder(args: list[str]) -> bool:
    name = None
    vendor = None
    qty = None

    if len(args) > 0:
        name = args[0]

    if len(args) > 1:
        vendor = args[1]

    if len(args) > 2:
        result = try_parse_float(args[2])

        if not result[0]:
            return False

        qty = result[1]

    order_manager.cart_remove(name, vendor, qty)
    return True


def print_help():
    print("Usage:")
    print()
    print("q - Quit")
    print()
    print("add name:str quantity:float [category:str] [brand:str]\n"
          "- Add (quantity) amount of (name) to the inventory, with optional category and brand.\n"
          "- Negative quantity means removing.")
    print()
    print("list - List the current inventory")
    print()
    print("order name:str quantity:float [vendor:str]\n"
          "- Add an order for (quantity) amount of (name) to the cart, optionally specifying a vendor.\n"
          "- If no vendor specified will use the one with best price.")
    print()
    print("delorder [name:str] [vendor:str] [quantity:float]\n"
          "- If no name, vendor, quantity specified, will clear the current cart.\n"
          "- If only name specified, will clear all orders of (name) in cart.\n"
          "- If name and vendor specified, will clear all orders of (name) with this vendor in cart.\n"
          "- Otherwise, reduce an order by (quantity) amount for (name) in the cart, with the specified vendor.")
    print()
    print("cart - View the contents of the current cart.")
    print()
    print("checkout - Complete and send the orders in the cart to corresponding vendors.")
    print()
    print("low - Check the items with quantity below a predefined threshold.")
    print()
    print("refill - Place orders in the cart for items with low inventory.")
    print()
    print("toprecipes n:int\n"
          "- View the top n best recipes for the current inventory.")
    print()
    print("recipe name:str\n"
          "- View the recipe and inventory difference.")
    print()


if __name__ == "__main__":
    is_running = True
    order_manager = OrderManager([Supermarket("Coles"), Supermarket("Woolworth")])
    inv_manager = InventoryManager(order_manager)
    inv_manager.refresh_inventory()
    recipes = Recipes()

    while is_running:
        if process_cmds(shlex.split(input("Enter command: "))):
            print()
            print("-" * 40)
        else:
            print("Invalid command")
            print()
            print_help()
